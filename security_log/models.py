from django.db import models
from django_mysql.models import EnumField, FixedCharField
from django.conf import settings
User = settings.AUTH_USER_MODEL


class LogTypeChoice(models.TextChoices):
    offline = "offline"
    disable_tracking = "disable tracking"
    changes_datetime = "changes datetime"


class TblSecurityLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    log_type = EnumField(
        blank=True, null=True, choices=LogTypeChoice.choices, db_column="fld_log_type")
    device_info = FixedCharField(
        max_length=255, blank=True, null=True, db_column="fld_device_info")
    ip_address = FixedCharField(
        max_length=100, blank=True, null=True, db_column="fld_ip_address")
    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(default=False, db_column="fld_is_delete")
    created_datetime = models.DateField(
        auto_now_add=True, db_column="fld_created_datetime")

    # def __str__(self) -> str:
    #     return self.site_name

    class Meta:
        managed = True
        db_table = 'tbl_security_log'
