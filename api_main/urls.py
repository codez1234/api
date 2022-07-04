from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


def home(request):
    return HttpResponse("hello")


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('notification/', include('notifications.urls'))

]
# if settings.DEBUG:
# urlpatterns += static(settings.MEDIA_URL,
#                       document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve,
                        {'document_root': settings.MEDIA_ROOT, }), ]

admin.site.site_header = "OMC Power Manage"
admin.site.index_title = "OMC Power Manage"
admin.site.site_title = "OMC Power Portal"
