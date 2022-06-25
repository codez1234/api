from django.urls import path
from account.views import *
from notifications.views import SendPushNotifications
urlpatterns = [
    path('<str:function_name>', SendPushNotifications.as_view(),
         name='SendPushNotifications'),

]
