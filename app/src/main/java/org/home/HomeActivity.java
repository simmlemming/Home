package org.home;

import android.content.ComponentName;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;

import org.home.network.SendGcmTokenRequest;
import org.home.service.PubnubService;


public class HomeActivity extends AppCompatActivity implements View.OnClickListener {

    private ServiceConnection serviceConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
            service = ((PubnubService.LocalBinder) iBinder).service();

            service.setStateListener(new PubnubService.StateListener() {
                @Override
                public void hartbeatStateChanged(PubnubService service, boolean isHartbeating) {
                    updateUi();
                }

                @Override
                public void onHartbeatResult(PubnubService service, boolean ok) {
                    if (iconView != null) {
                        iconView.setImageResource(service.isHartbeating() && ok ? R.drawable.ic_notification_ok : R.drawable.ic_notification_fail);
                        animateIconView();
                    }
                }

                private void animateIconView() {
                    iconView.animate()
                            .alpha(0.5f)
                            .setDuration(250)
                            .withEndAction(new Runnable() {
                                @Override
                                public void run() {
                                    iconView.animate()
                                            .setDuration(100)
                                            .alpha(1f);
                                }
                            });
                }
            });

            updateUi();
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            service = null;
            updateUi();
        }
    };

    private PubnubService service;
    private View sendTokenView;
    private EditText deviceNameView, deviceTokenView;

    private ImageView iconView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        iconView = (ImageView) findViewById(R.id.icon);
        sendTokenView = findViewById(R.id.send_token);
        deviceNameView = (EditText) findViewById(R.id.device_name);
        deviceTokenView = (EditText) findViewById(R.id.device_token);

        sendTokenView.setOnClickListener(this);

        bindService(PubnubService.intent(this), serviceConnection, BIND_AUTO_CREATE);

        updateUi();
    }

    private void updateUi() {
//        startView.setEnabled(service != null && !service.isHartbeating());
//        stopView.setEnabled(service != null && service.isHartbeating());
//
//        if (service == null || !service.isHartbeating()) {
//            iconView.setImageResource(R.drawable.ic_notification_fail);
//        }
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.send_token:
                sendToken();
                break;
        }
    }

    private void sendToken() {
        String deviceName = deviceNameView.getText().toString();
        String deviceToken = deviceTokenView.getText().toString();

        SendGcmTokenRequest request = new SendGcmTokenRequest(deviceName, deviceToken);
        ((HomeApplication)getApplication()).getRequestQueue().add(request);
    }

    @Override
    protected void onDestroy() {
        if (service != null) {
            service.setStateListener(null);
            unbindService(serviceConnection);
        }

        super.onDestroy();
    }
}
