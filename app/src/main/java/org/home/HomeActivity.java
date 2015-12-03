package org.home;

import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;

import org.home.gcm.GcmRegistrationService;
import org.home.network.SendGcmTokenRequest;


public class HomeActivity extends AppCompatActivity implements View.OnClickListener {

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

        int playServicesAvailable = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
        if (playServicesAvailable == ConnectionResult.SUCCESS) {
            GcmRegistrationService.start(this);
        } else {
            Dialog dialog = GooglePlayServicesUtil.getErrorDialog(playServicesAvailable, this, 0, new DialogInterface.OnCancelListener() {
                @Override
                public void onCancel(DialogInterface dialog) {
                    finish();
                }
            });
            dialog.show();
        }
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
}
