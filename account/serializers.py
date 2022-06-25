from dataclasses import fields
from wsgiref.validate import validator
from rest_framework import serializers
from account.models import User
from database.models import TblAttendance, TblAttendanceLog, TblUserSites, TblSites, TblUserReimbursements, TblAttendanceLog
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from modules.errors import messages
import re
from django.core.validators import MaxValueValidator, MinValueValidator
from notifications.models import TblPushNotificationLog


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("id", 'password', "last_login", "is_active", "is_delete",
                   "datetime_timestamp", "is_admin", "user_level")


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError(
                messages.get("passwords_not_equal"))

        if len(password) < 9:
            raise serializers.ValidationError(
                messages.get("password_length"))

        if not re.findall('[A-Z]', password):
            raise serializers.ValidationError(
                messages.get("password_upper_case"))

        if not re.findall('[a-z]', password):
            raise serializers.ValidationError(
                messages.get("password_lower_case"))

        user.set_password(password)
        user.save()
        return attrs


# # +++++++++++++++++++++++++++++++++++++++++++++++++ #


class TblAttendanceSerializer(serializers.ModelSerializer):
    def on_fld_attendance_status(value):
        if value not in ["current", "check_in", "check_out"]:
            raise serializers.ValidationError(
                "please provide valid fld_attendance_status")

    fld_attendance_status = serializers.CharField(
        validators=[on_fld_attendance_status])
    fld_latitude = serializers.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])
    fld_longitude = serializers.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)])
    # fld_ip_address = serializers.CharField()
    fld_date = serializers.DateField()
    fld_time = serializers.TimeField()

    class Meta:
        model = TblAttendance
        fields = ("fld_user_id", "fld_attendance_status", "visit_id",
                  "fld_latitude", "fld_longitude", "fld_ip_address", "auto_check_out", "fld_date", "fld_time")

        def create(self, validated_data):
            return TblAttendance.objects.create(**validated_data)


class TblSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSites
        fields = ('site_omc_id', 'site_type', 'site_name', "state",
                  "district", "latitude", "longitude")


class TblUserSitesSerializer(serializers.ModelSerializer):
    # sites = TblSitesSerializer(read_only=True, many=True)

    class Meta:
        model = TblUserSites
        # fields = ("assigned_date", "created_datetime")
        exclude = ("id", "user_id", "sites", "is_active",
                   "is_delete", "created_datetime")


class UserReimbursementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblUserReimbursements
        # fields = "__all__"
        exclude = ("id", 'user_id', "is_active", "is_delete")


class TblSitesSerializer2(serializers.ModelSerializer):
    class Meta:
        model = TblSites
        fields = ('site_omc_id', 'site_type', 'site_name')


class TblAttendanceLogSerializer(serializers.ModelSerializer):
    site_id = TblSitesSerializer2(read_only=True)

    class Meta:
        model = TblAttendanceLog
        # fields = "__all__"
        # fields = ("site_id", "visit_id")
        exclude = ("id", 'user_id', "is_active",
                   "is_delete", "created_datetime")


class TblPushNotificationLogSerializer(serializers.ModelSerializer):

    date = serializers.DateField(source="getDate")
    time = serializers.TimeField(source="getTime")

    class Meta:
        model = TblPushNotificationLog
        fields = ("notification_title",
                  "notification_description", "date", "time")
