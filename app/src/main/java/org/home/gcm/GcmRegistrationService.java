package org.home.gcm;

/**
 * Created by mtkachenko on 02/12/15.
 */

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.google.android.gms.gcm.GoogleCloudMessaging;
import com.google.android.gms.iid.InstanceID;

import org.home.HomeApplication;
import org.home.R;
import org.home.network.SendGcmTokenRequest;

import java.io.IOException;

public class GcmRegistrationService extends IntentService {
    private static final String TAG = HomeApplication.TAG;

    public static void start(Context context) {
        Intent intent = new Intent(context, GcmRegistrationService.class);
        context.startService(intent);
    }

    public GcmRegistrationService() {
        super(TAG);
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        try {
            InstanceID instanceID = InstanceID.getInstance(this);
            String token = instanceID.getToken(getString(R.string.gcm_defaultSenderId), GoogleCloudMessaging.INSTANCE_ID_SCOPE, null);

            sendTokenToServer(token);
            Log.i(TAG, "Token received: " + token);
        } catch (IOException e) {
            Log.e(TAG, "Failed to complete token refresh", e);
        }
    }

    private void sendTokenToServer(String token) {
        SendGcmTokenRequest request = new SendGcmTokenRequest("test_device", token);
        ((HomeApplication)getApplication()).getRequestQueue().add(request);
    }
}
