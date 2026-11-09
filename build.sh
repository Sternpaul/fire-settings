#!/usr/bin/env bash
# Gradle-free build using Ubuntu's ARM-native packages:
#   apt install aapt apksigner zipalign dalvik-exchange android-sdk-platform-23
set -euo pipefail
cd "$(dirname "$0")"
ANDROID_JAR=/usr/lib/android-sdk/platforms/android-23/android.jar
KEYSTORE=keystore/release.jks
OUT=out
NAME=FireSettings

rm -rf "$OUT" && mkdir -p "$OUT"/{gen,classes,dex}

if [ ! -f "$KEYSTORE" ]; then
  mkdir -p keystore
  keytool -genkeypair -keystore "$KEYSTORE" -alias firesettings -keyalg RSA -keysize 2048 \
    -validity 10000 -storepass firesettings -keypass firesettings -dname "CN=Fire Settings"
fi

aapt package -f -m -J "$OUT/gen" -M AndroidManifest.xml -S res -I "$ANDROID_JAR"
javac --release 8 -nowarn -Xlint:-options -classpath "$ANDROID_JAR" -d "$OUT/classes" \
  $(find src "$OUT/gen" -name '*.java')
dalvik-exchange --dex --min-sdk-version=22 --output="$OUT/dex/classes.dex" "$OUT/classes"

aapt package -f -M AndroidManifest.xml -S res -I "$ANDROID_JAR" -F "$OUT/$NAME-unaligned.apk"
(cd "$OUT/dex" && aapt add "../$NAME-unaligned.apk" classes.dex >/dev/null)
zipalign -f -p 4 "$OUT/$NAME-unaligned.apk" "$OUT/$NAME-aligned.apk"
apksigner sign --ks "$KEYSTORE" --ks-pass pass:firesettings --key-pass pass:firesettings \
  --out "$OUT/$NAME.apk" "$OUT/$NAME-aligned.apk"
apksigner verify --verbose "$OUT/$NAME.apk"
echo "Built $(pwd)/$OUT/$NAME.apk"
