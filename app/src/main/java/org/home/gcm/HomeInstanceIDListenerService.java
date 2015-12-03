package org.home.gcm;

/**
 * Created by mtkachenko on 02/12/15.
 */
import com.google.android.gms.iid.InstanceIDListenerService;

public class HomeInstanceIDListenerService extends InstanceIDListenerService {
    /**
     * Called if InstanceID token is updated. This may occur if the security of
     * the previous token had been compromised. This call is initiated by the
     * InstanceID provider.
     */

    @Override
    public void onTokenRefresh() {
        GcmRegistrationService.start(getApplicationContext());
    }
}
