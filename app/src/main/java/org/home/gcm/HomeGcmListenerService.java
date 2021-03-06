/**
 * Copyright 2015 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.home.gcm;

import android.app.Notification;
import android.app.NotificationManager;
import android.content.Context;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.NotificationCompat;
import android.util.Log;

import com.google.android.gms.gcm.GcmListenerService;
import com.google.gson.Gson;

import org.home.HomeActivity;
import org.home.HomeApplication;
import org.home.R;
import org.home.model.Status;
import org.home.network.CurrentStatusRequest;

public class HomeGcmListenerService extends GcmListenerService {
    private static final int NOTIFICATION_ID = 0;

    /**
     * Called when message is received.
     *
     * @param from SenderID of the sender.
     * @param data Data bundle containing message data as key/value pairs.
     *             For Set of keys use data.keySet().
     */
    @Override
    public void onMessageReceived(String from, Bundle data) {
        String message = data.getString("message");
        Log.i("P", "From: " + from);
        Log.i("P", "Message: " + message);

        notifyMessageReceived(message);
    }

    private void notifyMessageReceived(final String message) {
        HomeApplication application = (HomeApplication) getApplication();

        sendEvent(message, application);

        if (!application.areSensorsOnScreen()) {
            showSystemNotification(application);
        }
    }

    private void sendEvent(String message, HomeApplication application) {
        Status status = new Gson().fromJson(message, Status.class);
        CurrentStatusRequest.StatusReceivedEvent event = new CurrentStatusRequest.StatusReceivedEvent(status);
        application.getEventBus().post(event);
    }

    private void showSystemNotification(HomeApplication application) {
        Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        android.support.v4.app.NotificationCompat.Builder builder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.drawable.ic_notification_ok)
                .setContentTitle("Home")
                .setContentText("Alert")
                .setAutoCancel(true)
                .setSound(defaultSoundUri)
                .setPriority(Notification.PRIORITY_MAX)
                .setContentIntent(HomeActivity.intentForNotification(application));

        NotificationManager notificationManager =
        (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        notificationManager.notify(NOTIFICATION_ID, builder.build());
    }
}
