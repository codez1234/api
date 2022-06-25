
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from account.phone_number_validation import check_phone_number
from account.serializers import *
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from modules.createOrWriteTextFile import request_text_file, response_text_file, date_now, get_visit_id_date
from modules.errors import messages
from modules.deviceCheck import check_device
from modules.ipAddress import validate_ip_address
from modules.geoBound import is_arrived
from django.shortcuts import get_object_or_404
from modules.getSites import get_sites
from datetime import datetime
from notifications.cronjob_notification import forget_check_in_push, forget_check_out_push


class SendPushNotifications(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, function_name, format=None):
        # print(function_name)
        if function_name == "forget_to_checkin":
            values = forget_check_in_push()
            return Response({"status": "success", 'message': "sent push"}, status=status.HTTP_200_OK)

        elif function_name == "forget_to_checkout":
            values = forget_check_out_push()
            return Response({"status": "success", 'message': "sent push"}, status=status.HTTP_200_OK)

        return Response({"status": "error", 'message': "this name does not exist"}, status=status.HTTP_404_NOT_FOUND)
