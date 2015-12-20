package org.home.network;

import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.home.HomeApplication;
import org.home.HomeEventBus;
import org.jetbrains.annotations.Nullable;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by mtkachenko on 01/12/15.
 */
public class SendGcmTokenRequest extends BaseRequest<SendGcmTokenRequest.SendGcmTokenResponse> {
    private final String deviceName;
    private final String token;

    public SendGcmTokenRequest(String deviceName, String token) {
        super(Method.POST, url("/device"), new OkListener(), new ErrorListener());
        this.deviceName = deviceName;
        this.token = token;
    }

    @Nullable
    @Override
    protected String getBodyAsString() {
        JSONObject body = new JSONObject();

        try {
            body.put("device_name", deviceName);
            body.put("device_token", token);
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }

        return body.toString();
    }

    @Override
    protected SendGcmTokenResponse parseNetworkResponse(@Nullable String data) {
        return new SendGcmTokenResponse();
    }

    private static class ErrorListener implements Response.ErrorListener {

        @Override
        public void onErrorResponse(VolleyError volleyError) {
            String errorMessage = volleyError.getMessage();

            if (volleyError.networkResponse != null && volleyError.networkResponse.data != null) {
                errorMessage = new String(volleyError.networkResponse.data);
            }

            Log.e(HomeApplication.TAG, "Cannot send device token: " + errorMessage);
            HomeEventBus.getDefault().post(new SendGcmTokenRequestFailedEvent(volleyError.getMessage()));
        }
    }

    private static class OkListener implements Response.Listener<SendGcmTokenResponse> {

        @Override
        public void onResponse(SendGcmTokenResponse sendGcmTokenResponse) {
            Log.i(HomeApplication.TAG, "Device token sent");
        }
    }

    public static class SendGcmTokenResponse {

    }

    public static class SendGcmTokenRequestFailedEvent extends RequestFailedEvent {

        public SendGcmTokenRequestFailedEvent(String userFriendlyErrorMessage) {
            super(userFriendlyErrorMessage);
        }
    }
}
