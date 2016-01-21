package org.home.network;

import org.jetbrains.annotations.Nullable;

/**
 * Created by mtkachenko on 21/01/16.
 */
public class ChangeModeRequest extends CurrentStatusRequest {
    public static final String TAG = "change_mode_request";
    private final String mode;

    public ChangeModeRequest(String mode) {
        super(Method.POST, url("/mode"));
        this.mode = mode;
        setTag(TAG);
    }

    @Nullable
    @Override
    protected String getBodyAsString() {
        return "{\"mode\":\"" + mode + "\"}";
    }
}
