from django.db import models
from django_mysql.models import EnumField, FixedCharField


class DeviceTypeChoice(models.TextChoices):
    android = "android"
    ios = "iso"


class Version(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    version_name = FixedCharField(
        blank=True, null=True, max_length=10, db_column="fld_version_name")
    type = EnumField(blank=True, null=True, choices=DeviceTypeChoice.choices,
                     default="android", db_column="fld_type")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")

    def __str__(self) -> str:
        return self.version_name

    class Meta:
        db_table = 'tbl_version_check'
