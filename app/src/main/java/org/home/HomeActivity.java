package org.home;

import android.app.Dialog;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;

import org.home.gcm.GcmRegistrationService;
import org.home.network.CurrentStatusRequest;
import org.home.network.SendGcmTokenRequest;


public class HomeActivity extends AppCompatActivity implements View.OnClickListener {
    private final static String EXTRA_STARTED_FROM_NOTIFICATION = "started_from_notification";

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

        boolean startedFromNotification = getIntent().getBooleanExtra(EXTRA_STARTED_FROM_NOTIFICATION, false);
        if (!startedFromNotification) {
            refreshGcmToken();
        }

        ((HomeApplication)getApplication()).getEventBus().register(this);

        CurrentStatusRequest request = new CurrentStatusRequest();
        ((HomeApplication)getApplication()).getRequestQueue().cancelAll(CurrentStatusRequest.TAG);
        ((HomeApplication)getApplication()).getRequestQueue().add(request);
    }

    private void refreshGcmToken() {
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

    @SuppressWarnings("unused")
    public void onEvent(CurrentStatusRequest.StatusRequestFailedEvent event) {
        Toast.makeText(this, event.userFriendlyErrorMessage, Toast.LENGTH_SHORT).show();
    }

    @SuppressWarnings("unused")
    public void onEvent(CurrentStatusRequest.StatusReceivedEvent event) {
        Toast.makeText(this, "Status received", Toast.LENGTH_SHORT).show();
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
        ((HomeApplication)getApplication()).getEventBus().unregister(this);
        super.onDestroy();
    }

    public static PendingIntent intentForNotification(Context context) {
        Intent homeActivity = new Intent(context, HomeActivity.class);
        homeActivity.putExtra(EXTRA_STARTED_FROM_NOTIFICATION, true);
        homeActivity.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP); // Clear everything on top
        homeActivity.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP); // Also re-create Home activity
        return PendingIntent.getActivity(context, 0, homeActivity, PendingIntent.FLAG_CANCEL_CURRENT); // Also re-create pending intent
    }
}
