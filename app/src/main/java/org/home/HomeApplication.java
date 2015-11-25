package org.home;

import android.app.Application;
import android.os.Handler;

import org.home.service.PubnubService;


/**
 * Created by mtkachenko on 24/11/15.
 */
public class HomeApplication extends Application {
    public static final String TAG = "Home";

    private Handler handler;

    @Override
    public void onCreate() {
        super.onCreate();

        handler = new Handler();

        startService(PubnubService.intent(this));
    }

    public void runOnUiThread(Runnable r) {
        handler.post(r);
    }
}
