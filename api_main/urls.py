from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def home(request):
    return HttpResponse("hello")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('notification/', include('notifications.urls'))

]
admin.site.site_header = "OMC Power Manage"
admin.site.index_title = "OMC Power Manage"
admin.site.site_title = "OMC Power Portal"
