package org.home.network;

import android.util.Log;

import com.android.volley.NetworkResponse;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonRequest;

import org.home.HomeApplication;
import org.home.HomeEventBus;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by mtkachenko on 01/12/15.
 */
public class SendGcmTokenRequest extends JsonRequest<SendGcmTokenRequest.SendGcmTokenResponse> {

    public SendGcmTokenRequest(String deviceName, String token) {
        super(Method.POST, url(), requestBody(deviceName, token), new OkListener(), new ErrorListener());
    }

    private static String requestBody(String deviceName, String token) {
        JSONObject body = new JSONObject();

        try {
            body.put("device_name", deviceName);
            body.put("device_token", token);
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }

        return body.toString();
    }

    private static String url() {
        return "http://80.240.140.181:8080/device";
    }

    @Override
    protected Response<SendGcmTokenResponse> parseNetworkResponse(NetworkResponse networkResponse) {
        return Response.success(new SendGcmTokenResponse(), null);
    }

    private static class ErrorListener implements Response.ErrorListener {

        @Override
        public void onErrorResponse(VolleyError volleyError) {
            String errorMessage = volleyError.getMessage();

            if (volleyError.networkResponse != null && volleyError.networkResponse.data != null) {
                errorMessage = new String(volleyError.networkResponse.data);
            }

            Log.i(HomeApplication.TAG, "Cannot send device token: " + errorMessage);
            HomeEventBus.getDefault().post(new RequestFailedEvent(volleyError.getMessage()));
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

    public static class RequestFailedEvent {
        public final String userFriendlyErrorMessage;

        public RequestFailedEvent(String userFriendlyErrorMessage) {
            this.userFriendlyErrorMessage = userFriendlyErrorMessage;
        }
    }
}
