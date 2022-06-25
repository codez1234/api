from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from database.models import TblUserLevel, TblRates


class UserManager(BaseUserManager):

    def create_superuser(self, email, mobile, password, **other_fields):

        other_fields.setdefault('is_admin', True)
        # other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Superuser must be assigned to is_admin=True.')
        if other_fields.get('is_active') is not True:
            raise ValueError(
                'Superuser must be assigned to is_active=True.')

        return self.create_user(email, mobile, password, **other_fields)

    def create_user(self, email, mobile, password, **other_fields):

        if not email:
            raise ValueError('User must have an email address')

        if not mobile:
            raise ValueError('User must have an phone number')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          mobile=mobile, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, db_column="fld_ai_id")
    email = models.EmailField(
        verbose_name='Email',
        max_length=100,
        unique=True, db_column="fld_email")
    mobile = models.CharField(
        max_length=100, unique=True, db_column="fld_mobile")
    password = models.CharField(max_length=255, db_column="fld_password")
    user_level = models.ForeignKey(
        TblUserLevel, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_level")
    first_name = models.CharField(
        max_length=100,  default=" ", db_column="fld_first_name")
    last_name = models.CharField(
        max_length=100,  default=" ", db_column="fld_last_name")
    address = models.CharField(
        max_length=255, default=" ", db_column="fld_address")
    travel_type = models.ForeignKey(
        TblRates, on_delete=models.SET_NULL, blank=True, null=True, db_column="fld_travel_type")
    check_in_time = models.TimeField(
        blank=True, null=True, db_column="fld_check_in_time")
    check_out_time = models.TimeField(
        blank=True, null=True, db_column="fld_check_out_time")
    last_login = models.DateTimeField(
        blank=True, null=True, verbose_name='last login', db_column="fld_last_login_datetime")
    is_active = models.BooleanField(
        default=True, db_column="fld_is_active")
    is_delete = models.BooleanField(
        default=False, db_column="fld_is_delete")
    created_datetime = models.DateTimeField(
        blank=True, null=True, db_column="fld_created_datetime")
    datetime_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="fld_datetime_timestamp")
    is_admin = models.BooleanField(default=False, db_column="fld_is_admin")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', "password"]  # these fields must be entered.

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'tbl_users'


class TblLoginLog(models.Model):
    fld_ai_id = models.BigAutoField(primary_key=True)
    # ENUM('login','logout','other'), DEFAULT 'other'
    fld_type = models.CharField(max_length=6, default="other")
    # ENUM('mobileapp','webadmin'), DEFAULT 'mobileapp'
    fld_app = models.CharField(max_length=9, default="mobileapp")
    fld_user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column="fld_user_id")
    fld_access_token = models.TextField(blank=True, null=True)
    fld_device = models.CharField(max_length=100, blank=True, null=True)
    fld_device_information = models.TextField(blank=True, null=True)
    fld_ip_address = models.CharField(max_length=100, blank=True, null=True)
    fld_is_active = models.BooleanField(default=True)  # DEFAULT '1'
    fld_is_delete = models.BooleanField(default=False)  # DEFAULT '0'
    fld_created_datetime = models.DateTimeField(
        blank=True, null=True, default=timezone.now)  # datetime.now , default=datetime.now()

    class Meta:
        managed = True
        db_table = 'tbl_login_log'
