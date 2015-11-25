package org.home.service;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;

import com.pubnub.api.Callback;
import com.pubnub.api.Pubnub;
import com.pubnub.api.PubnubError;
import com.pubnub.api.PubnubException;

import org.home.HomeApplication;
import org.home.R;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Created by mtkachenko on 24/11/15.
 */
public class PubnubService extends Service {
    public interface StateListener {
        void hartbeatStateChanged(PubnubService service, boolean isHartbeating);
        void onHartbeatResult(PubnubService service, boolean ok);
    }

    private final static int NOTIFICATION_ID = 1;
    private final static int HARTBEAT_PERIOD_MS = 2000;

    private Pubnub pubnub;
    private String homeUuid, mainChannelId;

    private Timer timer;
    private StateListener stateListener;

    public static Intent intent(Context context) {
        return new Intent(context, PubnubService.class);
    }

    @Override
    public void onCreate() {
        super.onCreate();

        homeUuid = getResources().getString(R.string.home_uuid);

        String pubKey = getResources().getString(R.string.pub_key);
        String subKey = getResources().getString(R.string.sub_key);
        mainChannelId = getResources().getString(R.string.main_channel_id);

        pubnub = new Pubnub(pubKey, subKey, true);
        pubnub.setUUID("client_1");

        subscribe(mainChannelId);
    }

    private void subscribe(String mainChannelId) {
        try {
            pubnub.subscribe(mainChannelId, new Callback() {

                @Override
                public void connectCallback(String channel, Object message) {
                    Log.i(HomeApplication.TAG, "connected, " + String.valueOf(message));
                    notifyConnected("Connected", "connected to main channel", R.drawable.ic_notification_ok);

                    ((HomeApplication)getApplication()).runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            startHartbeat();
                        }
                    });
                }

                @Override
                public void errorCallback(String channel, PubnubError error) {
                    notifyConnected("Not connected", error.getErrorString(), R.drawable.ic_notification_fail);
                }
            });
        } catch (PubnubException e) {
            notifyConnected("Not connected", e.getPubnubError().getErrorString(), R.drawable.ic_notification_fail);
        }
    }

    public void startHartbeat() {
        if (timer != null) {
            return;
        }

        timer = new Timer();

        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                pubnub.hereNow(mainChannelId, false, true, hartbeatCallback);
            }
        }, 0, HARTBEAT_PERIOD_MS);

        if (stateListener != null) {
            stateListener.hartbeatStateChanged(this, true);
        }
    }

    public void stopHartbeat() {
        notifyConnected("Connection unknown", "Hartbeat stopped", R.drawable.ic_notification_fail);
        timer.cancel();
        timer.purge();
        notificationManager().cancel(NOTIFICATION_ID);

        timer = null;

        if (stateListener != null) {
            stateListener.hartbeatStateChanged(this, false);
        }
    }

    public boolean isHartbeating() {
        return timer != null;
    }

    private Callback hartbeatCallback = new Callback() {

        @Override
        public void successCallback(String channel, Object message) {
            Log.i(HomeApplication.TAG, "Hartbeat");
            boolean result = false;

            try {
                result = isHomeOnline(message);
                if (result) {
                    notifyConnected("Connected", "Hartbeat OK", R.drawable.ic_notification_ok);
                } else {
                    notifyConnected("Not connected", "Hartbeat fail", R.drawable.ic_notification_fail);
                }
            } catch (JSONException e) {
                notifyConnected("Not connected", "Hartbeat error: " + e.getLocalizedMessage(), R.drawable.ic_notification_fail);
            } finally {
                deliverHartbeatResult(result);
            }
        }

        @Override
        public void errorCallback(String channel, PubnubError error) {
            notifyConnected("Not subscribed for presence", error.getErrorString(), R.drawable.ic_notification_fail);
        }
    };

    private boolean isHomeOnline(Object message) throws JSONException {
        if (!(message instanceof JSONObject)) {
            throw new JSONException("Not JSON");
        }

        JSONObject update = (JSONObject) message;
        JSONArray uuids = update.getJSONArray("uuids");

        for (int i = 0; i < uuids.length(); i++) {
            if (homeUuid.equals(uuids.getString(i))) {
                return true;
            }
        }

        return false;
    }

    private void notifyConnected(String title, String text, int icon) {
        Notification.Builder notification = new Notification.Builder(getApplicationContext());

        notification.setContentTitle(title);
        notification.setContentText(text);
        notification.setSmallIcon(icon);
        notification.setAutoCancel(false);
        notification.setOngoing(true);

        notificationManager().notify(NOTIFICATION_ID, notification.build());
    }

    private NotificationManager notificationManager() {
        return (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
    }

    public void setStateListener(StateListener stateListener) {
        this.stateListener = stateListener;
    }

    private void deliverHartbeatResult(final boolean result) {
        if (stateListener == null) {
            return;
        }

        ((HomeApplication)getApplication()).runOnUiThread(new Runnable() {
            @Override
            public void run() {
                stateListener.onHartbeatResult(PubnubService.this, result);
            }
        });
    }


    @Override
    public void onDestroy() {
        pubnub.unsubscribe(getResources().getString(R.string.main_channel_id));
        NotificationManager mNotificationManager = notificationManager();
        mNotificationManager.cancel(NOTIFICATION_ID);

        super.onDestroy();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return new LocalBinder();
    }

    public class LocalBinder extends Binder {

        public PubnubService service() {
            return PubnubService.this;
        }
    }
}
