
import requests
import json
from configuration.notification import notification_data
from notifications.models import TblUserFirebase, TblNotificationConfig, TblPushNotificationLog
from datetime import date, datetime
from database.models import *
from modules.createOrWriteTextFile import time_now, date_now, get_current_time


def send_notification(deviceToken=None, title=None, body=None, icon=None):
    serverToken = notification_data.get("serverToken")
    print(f'serverToken=============={serverToken}')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }
    body = {
        'notification': {'title': title,
                         'body': body,
                         #  'icon': icon
                         },
        'to':
        deviceToken,
        'priority': 'high',
        #   'data': dataPayLoad,
    }
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

    return response


def send_push_notification(user_id=None, notification_type="", site=" "):
    print(
        f'site ======================================= {site}')
    print(f'user_id================={user_id}')
    print(f'notification_type==========================={notification_type}')
    # print("main")
    return_value = False
    if user_id and str(notification_type):
        users = TblUserFirebase.objects.filter(
            user_id=user_id, is_send_push=True)

        try:
            notification_data = TblNotificationConfig.objects.filter(
                notification_type=notification_type).last()
            title = notification_data.notification_title
            body = notification_data.notification_body
            if notification_type == "site reached":
                try:
                    txt = notification_data.notification_title
                    txt = txt.replace("{%NAME%}", user_id.first_name)
                    txt = txt.replace("{%SITENAME%}", site)
                    title = txt
                except:
                    title = notification_data.notification_title
        except:
            notification_data = None
        if users and notification_data:
            date_and_time = datetime.now()
            for i in users:
                response_var = send_notification(
                    deviceToken=i.firebase_id, title=title, body=body)
                status_code = response_var.status_code
                success_status = response_var.json().get("success")
                is_success = False
                if status_code == 200 and success_status == 1:
                    is_success = True
                push_log = TblPushNotificationLog.objects.create(user_id=user_id, notification_type_id=notification_data,
                                                                 user_firebase=i, firebase_response=response_var.json(), notification_title=title,  status_code=status_code, is_success=is_success,
                                                                 datetime=date_and_time)
                if body:
                    push_log.notification_description = body
                else:
                    push_log.notification_description = " "

                push_log.save()

            return_value = True
            # print(
            #     f'return_value==================================={return_value}')

    return return_value


# x = send_notification(deviceToken="c1eWN81OQYOsI0ROZRvFn1:APA91bExR7uyRiwDrtZT_76ZvrE89CPw9B0FK9ZF6xbsMFPKS3LFtUkvc8Z6s-QXfNHxJhjzJgcf9wrNPhqM12tbAE_lwz7itJnQPWJod8HkTsRHiJvgDAj9fYvwm_U8jbiHipbQWDfi",
#                       title="None", body="U+1F600", icon="U+1F600")
# print(x)
