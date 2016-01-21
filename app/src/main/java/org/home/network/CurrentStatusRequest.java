package org.home.network;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.home.HomeEventBus;
import org.home.model.Status;
import org.jetbrains.annotations.Nullable;

/**
 * Created by mtkachenko on 20/12/15.
 */
public class CurrentStatusRequest extends BaseRequest<Status> {
    public static final String TAG = "current_status";

    public CurrentStatusRequest() {
        this(Method.GET, url("/status"));
    }

    protected CurrentStatusRequest(int method, String url) {
        super(method, url, new OKListener(), new ErrorListener());
        setTag(TAG);
    }

    @Override
    protected Status parseNetworkResponse(@Nullable String data) {
        return gson().fromJson(data, Status.class);
    }

    private static class OKListener implements Response.Listener<Status> {
        @Override
        public void onResponse(Status status) {
            StatusReceivedEvent event = new StatusReceivedEvent(status);
            HomeEventBus.getDefault().post(event);
        }
    }

    private static class ErrorListener implements Response.ErrorListener {
        @Override
        public void onErrorResponse(VolleyError volleyError) {
            StatusRequestFailedEvent event = new StatusRequestFailedEvent(volleyError.getMessage());
            HomeEventBus.getDefault().post(event);
        }
    }

    public static class StatusReceivedEvent {
        @Nullable
        public final Status status;

        public StatusReceivedEvent(@Nullable Status status) {
            this.status = status;
        }
    }

    public static class StatusRequestFailedEvent extends RequestFailedEvent{

        public StatusRequestFailedEvent(String userFriendlyErrorMessage) {
            super(userFriendlyErrorMessage);
        }
    }
}
