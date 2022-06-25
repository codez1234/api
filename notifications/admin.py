from django.contrib import admin


from .models import *


class TblUserFirebaseAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "is_send_push",
                    "created_datetime"]
    search_fields = ["id", "user_id__email", "user_id__id", "firebase_id"]


admin.site.register(TblUserFirebase, TblUserFirebaseAdmin)


class TblNotificationConfigAdmin(admin.ModelAdmin):
    list_display = ["id", "notification_type", "notification_title",
                    "created_datetime"]
    search_fields = ["id", "notification_type", "notification_title", ]


admin.site.register(TblNotificationConfig, TblNotificationConfigAdmin)


class TblPushNotificationLogAdmin(admin.ModelAdmin):
    list_display = ["id", "notification_type_id", "user_id", "status_code",
                    "created_datetime"]
    search_fields = ["id",
                     "user_id__email", "status_code"]


admin.site.register(TblPushNotificationLog, TblPushNotificationLogAdmin)
