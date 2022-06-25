from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.models import User, TblLoginLog
from database.models import TblUserDevices, TblUserSites, TblAttendanceLog, TblAttendanceLog
from account.phone_number_validation import check_phone_number
from account.serializers import *
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from modules.createOrWriteTextFile import request_text_file, response_text_file, date_now, get_visit_id_date
from modules.errors import messages
from modules.deviceCheck import check_device
from modules.ipAddress import validate_ip_address
from modules.distanceCalculation import total_distance
from modules.imeiNumber import isValidIMEI
from modules.geoBound import is_arrived
from django.shortcuts import get_object_or_404
from modules.getSites import get_sites
from datetime import datetime
from notifications.models import TblUserFirebase, TblPushNotificationLog
from notifications.send_notification import send_push_notification
from configuration.configuration import configurations
from appVersion.models import Version
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# ++++++++++++++++++++++++++++++++++++++++ #

# ++++++++++++++++++++++++++++++++++++++++++++++++ #

# Generate Token Manually


def get_tokens_for_user(user):
    tokens = RefreshToken.for_user(user)
    return {
        'access_token': str(tokens.access_token),
        'refresh_token': str(tokens),
        'user': {
            'user_id': user.id,
            'email': user.email,
            'phone_number': user.mobile,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        dir = "login"
        request_text_file(user=request.user,
                          value=request.data, dir=dir)
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get('password')
        email = ""
        print(request.data)
        if validate_ip_address(request.data.get('ip_address')) is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")}, dir=dir)
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if isValidIMEI(int(request.data.get('imei_number'))) is False:
            response_text_file(
                value={"status": "error", 'message': messages.get("IMEI_error")}, dir=dir)
            return Response({"status": "error", 'message': messages.get("IMEI_error")}, status=status.HTTP_400_BAD_REQUEST)

        if "@" in email_or_phone:
            email = email_or_phone
        else:
            validate_phone_number = check_phone_number(email_or_phone)
            user = {}
            try:
                user = User.objects.get(
                    mobile=validate_phone_number)
            except:
                user = {}
            if user:
                email = user.email
            else:
                (email, password) = (None, None)

        user = authenticate(email=email, password=password)

        if user is not None:
            # check device model..
            obj = check_device(user.id, request.data.get(
                'device_model'),  request.data.get('imei_number'))

            if obj is not None:
                """
                insert into TblUserFirebase
                  if "device_token"
                """
                token = get_tokens_for_user(user)

                if request.data.get("device_token"):
                    user_firebase_token, created = TblUserFirebase.objects.get_or_create(
                        user_id=user, device_info=request.data.get("device_model"), firebase_id=request.data.get("device_token"))

                # insert into "TblLoginLog"
                login_log_insert, created = TblLoginLog.objects.get_or_create(
                    fld_type="login", fld_app="mobileapp", fld_user_id=user, fld_access_token=token.get("access_token"), fld_device=obj.get("device"), fld_device_information=request.data.get(
                        'device_model'), fld_ip_address=request.data.get('ip_address')

                )
                response_text_file(user=user.email, value={"status": "success", 'message': messages.get(
                    "login_success"), "data": token}, dir=dir)
                return Response({"status": "success", 'message': messages.get("login_success"), "data": token}, status=status.HTTP_200_OK)
            response_text_file(user=user.email, value={
                               "status": "error", 'message': messages.get("device_information_error")}, dir=dir)
            return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)
        else:
            response_text_file(value={"status": "error", 'message': messages.get(
                "wrong_email_or_phone_and_password")}, dir=dir)
            return Response({"status": "error", 'message': messages.get("wrong_email_or_phone_and_password")}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dir = "profile"
        request_text_file(user=request.user, value=request.data, dir=dir)
        serializer = UserProfileSerializer(request.user)
        val = serializer.data
        val["omc_id"] = request.user.id
        response_text_file(user=request.user, value={
                           "status": "success", 'message': "user data", "data": val}, dir=dir)
        return Response({"status": "success", 'message': "user data", "data": val}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = "changepassword"
        request_text_file(user=request.user, value=request.data, dir=dir)
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if validate_ip_address(request.data.get('ip_address')) is None:
            response_text_file(
                value={"status": "error", 'message': messages.get("ip_error")}, dir=dir)
            return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

        if isValidIMEI(int(request.data.get('imei_number'))) is False:
            response_text_file(
                value={"status": "error", 'message': messages.get("IMEI_error")}, dir=dir)
            return Response({"status": "error", 'message': messages.get("IMEI_error")}, status=status.HTTP_400_BAD_REQUEST)

        obj = check_device(request.user.id, request.data.get(
            'device_model'),  request.data.get('imei_number'))

        if obj is not None:
            serializer = UserChangePasswordSerializer(
                data={"password": password, "password2": password2}, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            response_text_file(dir=dir, user=request.user,
                               value={"status": "success", 'message': messages.get("password_changed")})
            return Response({"status": "success", 'message': messages.get("password_changed")}, status=status.HTTP_200_OK)
        response_text_file(dir=dir, user=request.user, value={
            "status": "error", 'message': messages.get("device_information_error")})
        return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)


class UserSitesView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = "siteplan"
        user = request.user
        id = request.user.id
        request_text_file(dir=dir, user=user, value=request.data)
        try:
            if request.data.get("date"):
                date = request.data.get("date")
            else:
                date = date_now()

            sites = TblUserSites.objects.filter(
                user_id=id, assigned_date=date).last()

            serializer = TblUserSitesSerializer(sites)
            serializer_sites = TblSitesSerializer(
                get_sites(sites.sites), many=True)
            data = serializer.data
            data["sites"] = serializer_sites.data
            response_text_file(dir=dir, user=user, value={
                "status": "success", 'message': "user sites", "data": data})
            return Response({"status": "success", 'message': "user sites", "data": data}, status=status.HTTP_200_OK)

        except:
            val = messages.get("site_not_assined_yet")
            if date < date_now():
                response_text_file(dir=dir, user=user, value={
                    "status": "error", 'message': messages.get("site was not assined")})
                return Response({"status": "error", 'message': messages.get("site was not assined")}, status=status.HTTP_404_NOT_FOUND)
            response_text_file(dir=dir, user=user, value={
                               "status": "error", 'message': val})
            return Response({"status": "error", 'message': val}, status=status.HTTP_404_NOT_FOUND)


class UserTblAttendanceView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # is_active=True, is_delete=False,
        dir = "attendance"
        user_obj = request.user
        user = request.user.id
        user_check_out_time = request.user.check_out_time
        values = request.data.get('attendence')
        try:
            rate_per_km = request.user.travel_type.fld_rate
        except:
            rate_per_km = configurations.get(
                "rate per km if not available for a user")

        # print(f'rate_per_km=========================== {rate_per_km}')
        request_text_file(dir=dir, user=user_obj, value=values)
        try:
            sites_lst = TblUserSites.objects.filter(
                user_id=user, is_active=True, is_delete=False, assigned_date=date_now()).last()
            sites = get_sites(sites_lst.sites)

        except:
            response_text_file(dir=dir,
                               user=user_obj, value={
                                   "status": "error", 'message': messages.get("site_not_assined_yet")})
            return Response({
                            "status": "error", 'message': messages.get("site_not_assined_yet")}, status=status.HTTP_404_NOT_FOUND)
        sites_lat_lon = []
        sites_details = []  # site object
        for i in sites:
            sites_lat_lon.append(
                                (i.latitude, i.longitude))
            sites_details.append(i)  # site object
            # print((i.latitude, i.longitude))

        # print(f'sites_details == {sites_details}')

        for value in values:
            ip_address = value.get('ip_address')
            if validate_ip_address(ip_address) is None:
                response_text_file(dir=dir,
                                   user=user_obj, value={"status": "error", 'message': messages.get("ip_error")})
                return Response({"status": "error", 'message': messages.get("ip_error")}, status=status.HTTP_400_BAD_REQUEST)

            if isValidIMEI(int(value.get('imei_number'))) is False:
                response_text_file(dir=dir,
                                   user=user_obj, value={"status": "error", 'message': messages.get("IMEI_error")})
                return Response({"status": "error", 'message': messages.get("IMEI_error")}, status=status.HTTP_400_BAD_REQUEST)

            obj = check_device(user, value.get(
                'device_model'), value.get('imei_number'))

            if obj is not None:
                data = {}
                data["fld_attendance_status"] = value.get("attendance_status")
                data["fld_latitude"] = value.get("latitude")
                data["fld_longitude"] = value.get("longitude")
                data["fld_date"] = value.get("date")
                data["fld_time"] = value.get("time")
                data["fld_user_id"] = user
                data["fld_ip_address"] = ip_address
                data["auto_check_out"] = False
                data["visit_id"] = f'OMCVISIT_{get_visit_id_date(date=value.get("date"))}_{user}'
                current_data_lat_lon = (
                    data["fld_latitude"], data["fld_longitude"])
                try:
                    previous_data = TblAttendance.objects.filter(
                        fld_user_id=user, fld_date=data["fld_date"]).last()
                except:
                    previous_data = None
                if previous_data:
                    # auto check-out code
                    if int(data["fld_time"].split(":")[0]) - int(user_check_out_time.strftime("%H")) >= configurations.get("auto check-out limit time"):
                        data["fld_attendance_status"] = "check_out"
                        data["auto_check_out"] = True
                    # auto check-out code ends.
                    # print(f'previous_data is available')

                    previous_data_lat_lon = (
                        previous_data.fld_latitude, previous_data.fld_longitude)

                    serializer = TblAttendanceSerializer(
                        data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        response_text_file(
                            dir=dir, user=user_obj, value=serializer.errors)
                        # print(serializer.errors)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    # execute rate code
                    user_reimbursement, created = TblUserReimbursements.objects.get_or_create(
                        user_id=request.user, is_active=True, is_delete=False, date=data["fld_date"], visit_id=data["visit_id"])
                    distance_calculated = total_distance(
                        [previous_data_lat_lon, current_data_lat_lon])

                    # =======================================code for amount cal. ==================

                    amount_calculation = distance_calculated * rate_per_km

                    previous_distance = user_reimbursement.distance
                    previous_amount = user_reimbursement.amount
                    user_reimbursement.distance = previous_distance + distance_calculated
                    user_reimbursement.amount = previous_amount + amount_calculation
                    user_reimbursement.save()
                    if is_arrived(current_data_lat_lon, sites_lat_lon) is not None:
                        value_for_list = is_arrived(
                            current_data_lat_lon, sites_lat_lon)  # return just index position.

                        # print(f'value_for_list == {value_for_list}')

                        user_attendence_log, created = TblAttendanceLog.objects.get_or_create(
                            user_id=request.user, site_id=sites_details[value_for_list], date=data["fld_date"], visit_id=data["visit_id"])

                        if created:
                            # send push
                            print("sent push notification")
                            site = user_attendence_log.site_id.site_name

                            send_push_notification_bool = send_push_notification(
                                user_id=request.user, notification_type="site reached", site=site)

                        if user_attendence_log.start_latitude:
                            user_attendence_log.end_latitude = data["fld_latitude"]
                            user_attendence_log.end_longitude = data["fld_longitude"]
                            user_attendence_log.end_time = data["fld_time"]
                            user_attendence_log.save()

                        else:
                            user_attendence_log.start_latitude = data["fld_latitude"]
                            user_attendence_log.start_longitude = data["fld_longitude"]
                            user_attendence_log.start_time = data["fld_time"]
                            user_attendence_log.end_latitude = data["fld_latitude"]
                            user_attendence_log.end_longitude = data["fld_longitude"]
                            user_attendence_log.end_time = data["fld_time"]
                            user_attendence_log.save()

                else:
                    if data["fld_attendance_status"] == "check_in":
                        # print(f'previous_data is not available')
                        serializer = TblAttendanceSerializer(
                            data=data)
                        if serializer.is_valid():
                            serializer.save()
                            user_reimbursement, created = TblUserReimbursements.objects.get_or_create(
                                user_id=request.user, is_active=True, is_delete=False, date=data["fld_date"], visit_id=data["visit_id"], distance=0.0, amount=0.0)

                            # print(current_data_lat_lon,
                            #       sites_lat_lon, user_reimbursement)

                            if is_arrived(current_data_lat_lon, sites_lat_lon) is not None:
                                value_for_list = is_arrived(
                                    current_data_lat_lon, sites_lat_lon)  # return just index position.
                                # caution point :-site_id = sites_details[value_for_list]
                                # be sure to verify
                                # print(
                                #     f'site_id = {sites_details[value_for_list]}')
                                user_attendence_log, created = TblAttendanceLog.objects.get_or_create(
                                    user_id=request.user, site_id=sites_details[value_for_list], date=data["fld_date"], visit_id=data["visit_id"], start_latitude=data["fld_latitude"], start_longitude=data["fld_longitude"], end_latitude=data["fld_latitude"], end_longitude=data["fld_longitude"], start_time=data["fld_time"], end_time=data["fld_time"])

                                if created:
                                    # send push
                                    print("sent push notification")
                                    site = user_attendence_log.site_id.site_name
                                    send_push_notification_bool = send_push_notification(
                                        user_id=request.user, notification_type="site reached", site=site)

                                # print("from else")

                        else:
                            response_text_file(dir=dir,
                                               user=user_obj, value=serializer.errors)
                            # print(serializer.errors)
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    else:

                        response_text_file(dir=dir,
                                           user=user_obj, value={
                                               "status": "error", 'message': messages.get("check_in_first")})
                        # print(serializer.errors)
                        return Response({
                            "status": "error", 'message': messages.get("check_in_first")}, status=status.HTTP_400_BAD_REQUEST)

            else:
                response_text_file(dir=dir, user=user_obj, value={
                    "status": "error", 'message': messages.get("device_information_error")})
                return Response({"status": "error", 'message': messages.get("device_information_error")}, status=status.HTTP_404_NOT_FOUND)

        response_text_file(dir=dir, user=user_obj, value={
            "status": "success", 'message': messages.get("data_created")})
        return Response({"status": "success", 'message': messages.get("data_created")}, status=status.HTTP_200_OK)


class AttendanceLogView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = "attendance_log"
        user = request.user
        user_check_out_time = request.user.check_out_time
        request_text_file(dir=dir, user=user, value=request.data)
        if request.data.get("date"):
            date = request.data.get("date")
        else:
            date = date_now()

        visit_id = f'OMCVISIT_{get_visit_id_date(date=date)}_{user.id}'
        obj = TblAttendanceLog.objects.filter(
            user_id=user, is_active=True, is_delete=False, date=date)
        serializer = TblAttendanceLogSerializer(obj, many=True)
        serializer_date = []
        for i in serializer.data:
            dict_data = {
                "site_omc_id": i.get("site_id")["site_omc_id"],
                "site_type": i.get("site_id")["site_type"],
                "site_name": i.get("site_id")["site_name"],
                "visit_id": i.get("visit_id"),
                "start_latitude": i.get("start_latitude"),
                "start_longitude": i.get("start_longitude"),
                "end_latitude": i.get("end_latitude"),
                "end_longitude": i.get("end_longitude"),
                "start_time": i.get("start_time"),
                "end_time": i.get("end_time"),
                "date": i.get("date")
            }
            serializer_date.append(dict_data)

        try:
            distance_obj = TblUserReimbursements.objects.filter(
                user_id=request.user, is_active=True, is_delete=False, visit_id=visit_id, date=date).first()
            total_distance = round(distance_obj.distance, 1)
            total_amount = int(distance_obj.amount)
            reimbursement_status = distance_obj.status
            minimum_value = configurations.get(
                "minimum total distance for claim reimbursements")
            minimum_time = configurations.get(
                "minimum time to show reimbursements button after check-out time")
            if total_distance < minimum_value or int(user_check_out_time.strftime("%H")) - int(datetime.now().strftime("%H")) >= minimum_time:
                reimbursement_status = "not_available"

        except:
            total_distance = 0.0
            total_amount = 0
            reimbursement_status = "not_available"

        response_text_file(dir=dir, user=request.user, value={
                           "status": "success", 'message': "user data", "data": {'visit_id': visit_id, "distance_travelled": total_distance, "total_amount": total_amount, "reimbursement_status": reimbursement_status, "attendancelog": serializer_date}})
        return Response({
            "status": "success", 'message': "user data", "data": {'visit_id': visit_id, "distance_travelled": total_distance, "total_amount": total_amount, "reimbursement_status": reimbursement_status, "attendancelog": serializer_date}}, status=status.HTTP_200_OK)


class UserReimbursementsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dir = "reimbursements"
        request_text_file(dir=dir, user=request.user, value=request.data)
        query_set = TblUserReimbursements.objects.exclude(status="pending").filter(
            user_id=request.user, is_active=True, is_delete=False, date__gte=datetime.now()-timedelta(days=7))
        serializer = UserReimbursementsSerializer(query_set, many=True)
        serializer_date = []
        # do this like "TblPushNotificationLogSerializer"
        for i in serializer.data:
            dict_data = {
                "claim_id": i.get("claim_id"),
                "visit_id": i.get("visit_id"),
                "distance": round(i.get("distance"), 1),
                "amount": i.get("amount"),
                "status": i.get("status").capitalize(),
                "date": i.get("date"),
            }
            serializer_date.append(dict_data)

        response_text_file(dir=dir, user=request.user, value={
            "status": "success", 'message': "", "data": {"reimbursement": serializer_date}})
        return Response({"status": "success", 'message': "", "data": {"reimbursement": serializer_date}}, status=status.HTTP_200_OK)


class ClaimReimbusmentsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = "claim_reimbursements"
        request_text_file(dir=dir, user=request.user, value=request.data)
        user = request.user
        visit_id = request.data.get("visit_id")
        try:
            reimbursement = TblUserReimbursements.objects.get(
                user_id=user, visit_id=visit_id, is_active=True, is_delete=False)
        except:
            response_text_file(dir=dir, user=request.user, value={
                               "status": "error", 'message': "please use valid visit id"})
            return Response({"status": "error", 'message': "please use valid visit id"}, status=status.HTTP_404_NOT_FOUND)
        if reimbursement.status == "pending":
            reimbursement.status = "requested"
            reimbursement.save()
            response_text_file(dir=dir, user=request.user, value={
                               "status": "success", 'message': "requested"})
            return Response({"status": "success", 'message': "requested"}, status=status.HTTP_200_OK)
        response_text_file(dir=dir, user=request.user, value={
                           "status": "success", 'message': "Already requested"})
        return Response({"status": "success", 'message': "Already requested"}, status=status.HTTP_200_OK)


class NotificationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dir = "notifications"
        user = request.user
        request_text_file(dir=dir, user=user, value=request.data)
        try:
            number_of_days = configurations.get(
                "number of days for list notification api data")
        except:
            number_of_days = 7
        obj = TblPushNotificationLog.objects.filter(
            user_id=user, is_success=True, is_active=True, is_delete=False, created_datetime__gte=datetime.now()-timedelta(days=number_of_days)).order_by('-id')

        serializer = TblPushNotificationLogSerializer(obj, many=True)
        response_text_file(dir=dir, user=user, value={
                           "notifications": serializer.data})

        return Response({"status": "success", 'message': "notifications", "data": {"notifications": serializer.data}}, status=status.HTTP_200_OK)


class VersionCheckView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = "version_check"
        request_text_file(dir=dir, user=request.user, value=request.data)
        current_app = Version.objects.filter(
            is_active=True, is_delete=False).last()
        if request.data.get("version") == current_app.version_name and request.data.get("type") == current_app.type:
            response_text_file(dir=dir, user=request.user, value={
                               "status": "success", 'message': ""})
            return Response({"status": "success", 'message': ""}, status=status.HTTP_200_OK)

        response_text_file(dir=dir, user=request.user, value={
            "status": "error", 'message': messages.get("app version check")})
        return Response({"status": "error", 'message': messages.get("app version check")}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        dir = "logout"
        user = request.user
        request_text_file(dir=dir, user=user, value=request.data)
        device_info = request.data.get("device_model")
        # access_token = request.headers.get("Authorization").split(" ")[-1]
        access_token = request.headers.get("Authorization")[7:]
        obj = check_device(user.id, device_info, None)

        if request.data.get("device_token"):
            user_firebase_token = TblUserFirebase.objects.filter(
                user_id=user, device_info=device_info, firebase_id=request.data.get("device_token")).last()
            if user_firebase_token:
                user_firebase_token.is_send_push = False
                user_firebase_token.save()

        # insert into "TblLoginLog"
        login_log_insert, created = TblLoginLog.objects.get_or_create(fld_type="logout", fld_app="mobileapp", fld_user_id=user, fld_access_token=access_token,
                                                                      fld_device_information=device_info, fld_device=obj.get("device"), fld_ip_address=request.data.get("ip_address"))

        response_text_file(dir=dir, user=request.user, value={
            "status": "success", 'message': "User Logged out successfully"})
        return Response({"status": "success", 'message': "User Logged out successfully"}, status=status.HTTP_200_OK)
