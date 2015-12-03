package org.home;

import android.app.Application;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Handler;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

import org.home.network.SendGcmTokenRequest;

import de.greenrobot.event.EventBus;


/**
 * Created by mtkachenko on 24/11/15.
 */
public class HomeApplication extends Application {
    public static final String TAG = "Home";

    private Handler handler;
    private RequestQueue requestQueue;
    private EventBus eventBus;

    @Override
    public void onCreate() {
        super.onCreate();

        handler = new Handler();

        requestQueue = Volley.newRequestQueue(this);
        requestQueue.start();

        eventBus = HomeEventBus.getDefault();
        eventBus.register(this);
    }

    @SuppressWarnings("unused")
    public void onEvent(SendGcmTokenRequest.RequestFailedEvent event) {
        getNotificationManager().notifyError(getString(R.string.error_cannot_send_gcm_token), event.userFriendlyErrorMessage);
    }

    public RequestQueue getRequestQueue() {
        return requestQueue;
    }

    public EventBus getEventBus() {
        return eventBus;
    }

    public void runOnUiThread(Runnable r) {
        handler.post(r);
    }

    public Settings getSettings() {
        return new Settings();
    }

    public HomeNotificationManager getNotificationManager() {
        return new HomeNotificationManager(this);
    }

    public class Settings {
        public static final String KEY_OLD_GCM_TOKEN = "org.home.old_gcm_token";

        private Settings() {
        }

        public void putString(String key, String value) {
            SharedPreferences.Editor settings = getSharedPreferences().edit();
            settings.putString(key, value);
            settings.apply();
        }

        public String getString(String key, String defaultValue) {
            return getSharedPreferences().getString(key, defaultValue);
        }

        public void putBoolean(String key, boolean value) {
            SharedPreferences.Editor settings = getSharedPreferences().edit();
            settings.putBoolean(key, value);
            settings.apply();
        }

        public boolean getBoolean(String key, boolean defaultValue) {
            return getSharedPreferences().getBoolean(key, defaultValue);
        }

        private SharedPreferences getSharedPreferences() {
            return HomeApplication.this.getSharedPreferences("org.home.prefs", Context.MODE_PRIVATE);
        }
    }
}
