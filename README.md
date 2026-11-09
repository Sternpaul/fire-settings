# Fire Settings

A small Fire TV app that opens the full Fire TV settings screen and then closes itself.

It's for launchers like Projectivy, whose "Android settings" button only flashes on Fire OS. Fire OS sends
`android.settings.SETTINGS` to Amazon's home screen, and the launcher intercepts it. Pin **Fire Settings**
to your home row to get a settings tile that works.

## What it does

The app has one Activity and no visible UI (`Theme.NoDisplay`). It starts
`com.amazon.tv.launcher/.ui.MainSettingsActivity`. If that screen can't be opened, it falls back to
`android.settings.SETTINGS`. Then it calls `finish()`.

Check that the target screen exists on your device:

```bash
adb shell am start -n com.amazon.tv.launcher/.ui.MainSettingsActivity
```

## Build

The build doesn't use Gradle. It runs on ARM64 (and x86) Ubuntu with the distro packages:

```bash
sudo apt install openjdk-17-jdk-headless aapt apksigner zipalign dalvik-exchange android-sdk-platform-23
./build.sh
```

The output is `out/FireSettings.apk`. On the first run, `build.sh` creates a signing key in `keystore/`
(git ignores it). Keep that key: updates with `adb install -r` only work when every version is signed
with the same key.

The icon and banner come from `tools/make_images.py` (needs Pillow):

```bash
python3 tools/make_images.py res/drawable-xhdpi
```

## Install

```bash
adb install -r out/FireSettings.apk
```
