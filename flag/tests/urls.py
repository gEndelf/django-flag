from django.conf.urls import include, url

app_name = 'flag'
urlpatterns = [
    url(r'^flag/', include('flag.urls')),
]
