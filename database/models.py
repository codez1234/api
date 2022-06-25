from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_mysql.models import EnumField, FixedCharField
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Audittrail(models.Model):
    datetime = models.DateTimeField()
    script = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    table = models.CharField(max_length=255, blank=True, null=True)
    field = models.CharField(max_length=255, blank=True, null=True)
    keyvalue = models.TextField(blank=True, null=True)
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audittrail'


class Subscriptions(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    endpoint = models.TextField()
    publickey = models.CharField(max_length=255)
    authenticationtoken = models.CharField(max_length=255)
    contentencoding = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'subscriptions'


class TblAdmin(models.Model):
    fld_ai_id = models.BigAutoField(primary_key=True)
    fld_name = models.CharField(max_length=100, blank=True, null=True)
    fld_username = models.CharField(max_length=100, blank=True, null=True)
    fld_password = models.CharField(max_length=255, blank=True, null=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_admin'


class AttendanceStatusChoice(models.TextChoices):
    check_in = "check_in"
    current = "current"
    check_out = "check_out"


class TblAttendance(models.Model):

    fld_ai_id = models.BigAutoField(primary_key=True)
    fld_user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")

    fld_attendance_status = EnumField(
        blank=True, null=True, choices=AttendanceStatusChoice.choices)

    fld_latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], blank=True, null=True)
    fld_longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True, null=True)
    fld_device_info = models.CharField(max_length=100, blank=True, null=True)
    fld_ip_address = models.CharField(max_length=100, blank=True, null=True)
    visit_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_visit_id")
    auto_check_out = models.BooleanField(
        default=False, db_column="fld_auto_check_out")
    fld_is_active = models.BooleanField(default=True)
    fld_is_delete = models.BooleanField(default=False)
    fld_date = models.DateField(blank=True, null=True)
    fld_time = models.TimeField(blank=True, null=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_attendance'


class FldTypeChoice(models.TextChoices):
    two_wheeler = "two_wheeler"
    four_wheeler = "four_wheeler"
    others = "others"


class TblRates(models.Model):
    fld_ai_id = models.AutoField(primary_key=True)
    fld_type = EnumField(blank=True, null=True, choices=FldTypeChoice.choices,
                         default="others", db_column="fld_type")
    fld_state = models.CharField(max_length=50, blank=True, null=True)
    fld_rate = models.PositiveSmallIntegerField(blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.fld_type

    class Meta:
        managed = True
        db_table = 'tbl_rates'


class TblSites(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    site_omc_id = models.CharField(
        max_length=10, blank=True, null=True, db_column="fld_site_omc_id")
    site_type = models.CharField(
        max_length=6, blank=True, null=True, db_column="fld_site_type")
    site_name = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_site_name")
    state = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_state")
    district = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_district")
    latitude = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_latitude")
    longitude = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_longitude")
    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(default=False, db_column="fld_is_delete")
    created_datetime = models.DateField(
        auto_now_add=True, db_column="fld_created_datetime")

    def __str__(self) -> str:
        return self.site_name

    class Meta:
        managed = True
        db_table = 'tbl_sites'


class TblUserDevices(models.Model):
    fld_ai_id = models.BigAutoField(primary_key=True)
    fld_user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    fld_device_model = models.CharField(max_length=100, blank=True, null=True)
    fld_imei_1 = models.CharField(max_length=100, blank=True, null=True)
    fld_imei_2 = models.CharField(max_length=100, blank=True, null=True)
    fld_device_id_token = models.CharField(
        max_length=255, blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_user_devices'

    def __str__(self) -> str:
        return self.fld_user_id.email


class TblUserLevel(models.Model):
    fld_ai_id = models.AutoField(primary_key=True)
    fld_user_level_name = models.CharField(
        max_length=20, blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)
    fld_created_datetime = models.DateTimeField(
        auto_now_add=True)

    def __str__(self) -> str:
        return str(self.fld_ai_id)

    class Meta:
        managed = True
        db_table = 'tbl_user_level'


class TblUserSites(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    sites = models.CharField(max_length=255, blank=True,
                             null=True, db_column="fld_sites")
    assigned_date = models.DateField(
        blank=True, null=True, db_column="fld_assigned_date")
    is_active = models.BooleanField(default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        auto_now_add=True, db_column="fld_created_datetime")

    class Meta:
        managed = True
        db_table = 'tbl_user_sites'


class ReimbursementStatusChoice(models.TextChoices):
    approved = "approved"
    pending = "pending"
    requested = "requested"
    closed = "closed"


class TblUserReimbursements(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    claim_id = models.CharField(
        max_length=100, blank=True, null=True, db_column="fld_claim_id")
    visit_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_visit_id")
    distance = models.FloatField(
        blank=True, null=True, db_column="fld_distance")
    amount = models.FloatField(
        blank=True, null=True, db_column="fld_amount")
    status = EnumField(blank=True, null=True, choices=ReimbursementStatusChoice.choices,
                       default="pending", db_column="fld_status")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")
    date = models.DateField(blank=True, null=True, db_column="fld_date")
    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")

    def getAmountInt(self):
        return int(self.amount)

    class Meta:
        db_table = 'tbl_user_reimbursements'


class TblAttendanceLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="fld_ai_id")
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    site_id = models.ForeignKey(
        TblSites, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_site_omc_id")
    visit_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="fld_visit_id")

    start_latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], blank=True, null=True, db_column="fld_start_latitude")
    start_longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True, null=True, db_column="fld_start_longitude")
    end_latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], blank=True, null=True, db_column="fld_end_latitude")
    end_longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True, null=True,
        db_column="fld_end_longitude")
    start_time = models.TimeField(
        blank=True, null=True, db_column="fld_start_time")
    end_time = models.TimeField(
        blank=True, null=True, db_column="fld_end_time")
    date = models.DateField(blank=True, null=True, db_column="fld_date")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")

    class Meta:
        db_table = 'tbl_attendance_log'
