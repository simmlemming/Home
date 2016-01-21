package org.home;

import android.app.Dialog;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;

import org.home.gcm.GcmRegistrationService;
import org.home.model.Status;
import org.home.network.ChangeModeRequest;
import org.home.network.CurrentStatusRequest;
import org.jetbrains.annotations.Nullable;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import static org.home.HomeApplication.MODE_GUARD;
import static org.home.HomeApplication.MODE_OFF;


public class HomeActivity extends AppCompatActivity implements View.OnClickListener {
    private final static String EXTRA_STARTED_FROM_NOTIFICATION = "started_from_notification";
    private final DateFormat DATE_FORMAT = new SimpleDateFormat("EEE, MMM d, HH:mm", Locale.getDefault());

    private RecyclerView sensorsView;
    private ImageView iconView;
    private TextView timeView;
    private Switch modeView;

    private Status status;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        iconView = (ImageView) findViewById(R.id.icon);
        sensorsView = (RecyclerView) findViewById(R.id.sensors);
        timeView = (TextView) findViewById(R.id.time);
        modeView = (Switch) findViewById(R.id.mode);

        sensorsView.setLayoutManager(new LinearLayoutManager(this));
        sensorsView.setAdapter(new SensorsAdapter(status));

        // Before listeners are set
        updateUi();

        iconView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                requestCurrentStatus();
            }
        });


        modeView.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                String mode = isChecked ? MODE_GUARD : MODE_OFF;
                ChangeModeRequest request = new ChangeModeRequest(mode);
                getHomeApplication().getRequestQueue().cancelAll(ChangeModeRequest.TAG);
                getHomeApplication().getRequestQueue().add(request);
            }
        });

        boolean startedFromNotification = getIntent().getBooleanExtra(EXTRA_STARTED_FROM_NOTIFICATION, false);
        if (!startedFromNotification) {
            refreshGcmToken();
        }

        ((HomeApplication)getApplication()).getEventBus().register(this);
        requestCurrentStatus();
    }

    @Override
    protected void onStart() {
        super.onStart();
        getHomeApplication().setSensorsOnScreen(true);
    }

    private void updateUi() {
        if (status == null) {
            timeView.setText(null);
            modeView.setEnabled(false);
        } else {
            modeView.setEnabled(true);
            modeView.setChecked(!status.mode.equals(MODE_OFF));
            timeView.setText(DATE_FORMAT.format(new Date(status.time * 1000l)));
        }

        ((SensorsAdapter)sensorsView.getAdapter()).setStatus(status);
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
        updateUi();
    }

    @SuppressWarnings("unused")
    public void onEventMainThread(CurrentStatusRequest.StatusReceivedEvent event) {
        status = event.status;
        updateUi();
    }

    @Override
    public void onClick(View view) {
    }

    private void requestCurrentStatus() {
        CurrentStatusRequest request = new CurrentStatusRequest();
        getHomeApplication().getRequestQueue().cancelAll(CurrentStatusRequest.TAG);
        getHomeApplication().getRequestQueue().add(request);
    }

    @Override
    protected void onStop() {
        getHomeApplication().setSensorsOnScreen(false);
        super.onStop();
    }

    @Override
    protected void onDestroy() {
        ((HomeApplication)getApplication()).getEventBus().unregister(this);
        super.onDestroy();
    }

    private HomeApplication getHomeApplication() {
        return (HomeApplication) getApplication();
    }

    public static class SensorsAdapter extends RecyclerView.Adapter<SensorsAdapter.SensorViews> {
        @Nullable private Status status;

        public SensorsAdapter(@Nullable Status status) {
            this.status = status;
        }

        @Override
        public SensorViews onCreateViewHolder(ViewGroup parent, int viewType) {
            View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.sensor_item, parent, false);
            return new SensorViews(itemView);
        }

        @Override
        public void onBindViewHolder(SensorViews holder, int position) {
            assert status != null;
            holder.fill(status.sensors.get(position));
        }

        @Override
        public int getItemCount() {
            return status == null ? 0 : status.sensors.size();
        }

        public void setStatus(@Nullable Status status) {
            this.status = status;
            notifyDataSetChanged();
        }

        public static class SensorViews extends RecyclerView.ViewHolder {
            private final TextView titleView;
            private final View statusView;

            public SensorViews(View itemView) {
                super(itemView);
                titleView = (TextView) itemView.findViewById(R.id.title);
                statusView = itemView.findViewById(R.id.icon_status);
            }

            private void fill(Status.Sensor sensor) {
                titleView.setText(sensor.name);
                statusView.setBackgroundResource(sensor.state == 1 ? R.drawable.ic_state_error : R.drawable.ic_state_ok);
            }
        }
    }

    public static PendingIntent intentForNotification(Context context) {
        Intent homeActivity = new Intent(context, HomeActivity.class);
        homeActivity.putExtra(EXTRA_STARTED_FROM_NOTIFICATION, true);
        homeActivity.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP); // Clear everything on top
        homeActivity.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP); // Also re-create Home activity
        return PendingIntent.getActivity(context, 0, homeActivity, PendingIntent.FLAG_CANCEL_CURRENT); // Also re-create pending intent
    }
}
