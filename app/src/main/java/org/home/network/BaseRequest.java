package org.home.network;

import android.util.Log;

import com.android.volley.NetworkResponse;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.JsonRequest;
import com.google.gson.Gson;

import org.home.HomeApplication;
import org.jetbrains.annotations.Nullable;

import java.io.UnsupportedEncodingException;

/**
 * Created by mtkachenko on 20/12/15.
 */
public abstract class BaseRequest<T> extends JsonRequest<T> {

    public BaseRequest(int method, String url, Response.Listener<T> listener, Response.ErrorListener errorListener) {
        super(method, url, null, listener, errorListener);
    }

    /** *
     * @param path with leading slash.
     */
    protected static String url(String path) {
        String url = "http://80.240.140.181:8080" + path;
//        String url = "http://192.168.56.1:8080" + path;
        Log.i(HomeApplication.TAG, url);
        return url;
    }

    @Override
    protected Response<T> parseNetworkResponse(NetworkResponse networkResponse) {
        String dataAsString = null;

        if (networkResponse.data != null) {
            dataAsString = new String(networkResponse.data);
            Log.d(HomeApplication.TAG, dataAsString);
        }

        T response = parseNetworkResponse(dataAsString);
        return Response.success(response, HttpHeaderParser.parseCacheHeaders(networkResponse));
    }

    @Override
    protected VolleyError parseNetworkError(VolleyError volleyError) {
        Log.e(HomeApplication.TAG, volleyError.getMessage());
        return super.parseNetworkError(volleyError);
    }

    protected abstract T parseNetworkResponse(@Nullable String data);

    protected Gson gson() {
        return new Gson();
    }

    @Nullable
    protected String getBodyAsString() {
        return null;
    }

    public byte[] getBody() {
        String body = getBodyAsString();

        try {
            return body == null ? null : body.getBytes("utf-8");
        } catch (UnsupportedEncodingException e) {
            Log.e(HomeApplication.TAG, String.format("Unsupported Encoding while trying to get the bytes of %s using %s", body, "utf-8"), e);
            return null;
        }
    }

    public static class RequestFailedEvent {
        public final String userFriendlyErrorMessage;

        public RequestFailedEvent(String userFriendlyErrorMessage) {
            this.userFriendlyErrorMessage = userFriendlyErrorMessage;
        }
    }
}
