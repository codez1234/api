from django.db import models
from django_mysql.models import EnumField, FixedCharField
from datetime import datetime, timedelta
from django.conf import settings
User = settings.AUTH_USER_MODEL


class TblUserFirebase(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    firebase_id = FixedCharField(
        max_length=255, blank=True, null=True, default="NA", db_column="fld_firebase_id")
    is_send_push = models.BooleanField(
        default=True, db_column="fld_is_send_push")
    device_info = FixedCharField(
        max_length=200, default="NA", db_column="fld_device_info")
    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        auto_now_add=True, db_column="fld_created_datetime")

    def __str__(self) -> str:
        return f'{self.user_id.email} on {str(self.created_datetime)}'

    class Meta:
        managed = True
        db_table = 'tbl_user_firebase'


class TblNotificationConfigStatusChoice(models.TextChoices):
    forgets_to_check_in = "forgets to check-in"
    forgets_to_check_out = "forgets to check-out"
    site_reached = "site reached"
    offline = "offline"
    outside_of_geolocation_bound = "outside of geolocation bound"
    disable_tracking = "disable tracking"
    changes_datetime = "changes datetime"


class TblNotificationConfig(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")

    notification_type = EnumField(
        blank=True, null=True, choices=TblNotificationConfigStatusChoice.choices, db_column="fld_notification_type")
    notification_title = FixedCharField(
        max_length=100, blank=True, null=True, default="NA", db_column="fld_notification_title")

    notification_body = FixedCharField(
        max_length=200, blank=True, null=True, default="NA", db_column="fld_notification_body")

    notification_icon = models.CharField(
        max_length=255, blank=True, null=True, default="NA", db_column="fld_notification_icon")

    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        auto_now_add=True, db_column="fld_created_datetime")

    def __str__(self) -> str:
        return self.notification_type

    class Meta:
        managed = True
        db_table = 'tbl_notification_config'


class TblPushNotificationLog(models.Model):

    id = models.AutoField(primary_key=True, db_column="fld_ai_id")

    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")

    notification_type_id = models.ForeignKey(
        TblNotificationConfig, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_notification_type_id")

    user_firebase = models.ForeignKey(
        TblUserFirebase, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_firebase")

    firebase_response = models.TextField(
        blank=True, null=True, default="NA", db_column="fld_firebase_response")

    status_code = FixedCharField(
        max_length=5, blank=True, null=True, default="NA", db_column="fld_status_code")

    notification_title = FixedCharField(
        max_length=100, default="NA", blank=True, null=True, db_column="fld_notification_title")
    notification_description = FixedCharField(
        max_length=200, default="NA", blank=True, null=True, db_column="fld_notification_description")

    is_success = models.BooleanField(default=True,  db_column="fld_is_success")

    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(default=False, db_column="fld_is_delete")
    datetime = models.DateTimeField(
        db_column="fld_datetime")

    created_datetime = models.DateTimeField(
        auto_now_add=True, db_column="fld_created_datetime")

    def getDate(self):
        suffix = {
            "01": "st",
            "02": "nd",
            "03": "rd",
        }
        notification_date = self.created_datetime.date()
        suffix_key = notification_date.strftime("%d")
        today = datetime.now().date()
        if notification_date == today:
            return "Today"
        elif today - timedelta(days=1) == notification_date:
            return "Yesterday"
        date_in_str = notification_date.strftime("%dth%B,%Y")
        if suffix_key in suffix.keys():
            return date_in_str.replace("th", suffix.get(suffix_key))
        return date_in_str

    def getTime(self):
        # return self.created_datetime.time().strftime("%H:%M") # in 24hr format
        return self.created_datetime.time().strftime("%I:%M %p")

    def __str__(self) -> str:
        return self.user_id.email

    class Meta:
        managed = True
        db_table = 'tbl_push_notification_log'
