package org.home;

import android.app.Notification;
import android.content.Context;

/**
 * Created by mtkachenko on 03/12/15.
 */
class HomeNotificationManager {
    private static final int ERROR_ICON = R.drawable.ic_notification_fail;
    private static final int NOTIFICATION_ID = 1;
    private final Context context;

    HomeNotificationManager(Context context) {
        this.context = context;
    }

    void notifyError(CharSequence title, CharSequence text) {
        Notification.Builder notification = new Notification.Builder(context);

        notification.setContentTitle(title);
        notification.setContentText(text);
        notification.setSmallIcon(ERROR_ICON);
        notification.setAutoCancel(true);
//        notification.setOngoing(true);
        notification.setContentIntent(HomeActivity.intentForNotification(context));

        notificationManager().notify(NOTIFICATION_ID, notification.build());
    }

    private android.app.NotificationManager notificationManager() {
        return (android.app.NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
    }

}
