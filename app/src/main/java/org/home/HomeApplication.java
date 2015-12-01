package org.home;

import android.app.Application;
import android.os.Handler;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

import org.home.service.PubnubService;


/**
 * Created by mtkachenko on 24/11/15.
 */
public class HomeApplication extends Application {
    public static final String TAG = "Home";

    private Handler handler;
    private RequestQueue requestQueue;

    @Override
    public void onCreate() {
        super.onCreate();

        handler = new Handler();

        requestQueue = Volley.newRequestQueue(this);
        requestQueue.start();

        startService(PubnubService.intent(this));
    }

    public RequestQueue getRequestQueue() {
        return requestQueue;
    }

    public void runOnUiThread(Runnable r) {
        handler.post(r);
    }
}
