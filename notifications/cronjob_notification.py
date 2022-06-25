from database.models import *
from datetime import datetime
from modules.createOrWriteTextFile import time_now, date_now, get_current_time
from notifications.send_notification import send_notification, send_push_notification
from configuration.configuration import configurations


def forget_check_in_push():
    sites = TblUserSites.objects.filter(assigned_date=date_now())
    current_time = get_current_time()
    for i in sites:
        user_obj = i.user_id
        user_time = str(user_obj.check_in_time)
        attendance = TblAttendance.objects.filter(
            fld_user_id=user_obj, fld_attendance_status="check_in", fld_date=date_now())

        if attendance:
            continue
        elif user_time <= current_time:
            # user.objects.filter(check_in_time__lte=datetime.now())
            send_push_notification(
                user_id=user_obj, notification_type="forgets to check-in")
            continue


def forget_check_out_push():
    sites = TblUserSites.objects.filter(assigned_date=date_now())
    for i in sites:
        user_obj = i.user_id
        user_time = user_obj.check_out_time
        attendance = TblAttendance.objects.filter(
            fld_user_id=user_obj, fld_date=date_now()).last()

        if attendance:
            if attendance.fld_attendance_status == "check_out":
                continue
            elif int(datetime.now().strftime("%H")) - int(user_time.strftime("%H")) >= configurations.get("check-out notification limit time"):
                send_push_notification(
                    user_id=user_obj, notification_type="forgets to check-out")
                continue
        continue
