package local.firesettings;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;

/** No UI: jump straight into Fire TV's full settings screen, then get out of the way. */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent fire = new Intent()
                .setClassName("com.amazon.tv.launcher",
                              "com.amazon.tv.launcher.ui.MainSettingsActivity")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            startActivity(fire);
        } catch (RuntimeException e) { // ActivityNotFoundException or SecurityException
            try {
                startActivity(new Intent(Settings.ACTION_SETTINGS)
                        .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
            } catch (RuntimeException ignored) {
            }
        }
        finish();
    }
}
