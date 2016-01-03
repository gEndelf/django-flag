"""
Urls for the django-flag app
Add a line like above to your own urls.py:
    ur(r'^flag/', include('flag.urls')),
To use the "flag_confirm" url, you can use the "flag_confirm_url" filter
in your template, or "get_confirm_url_for_object" helper in flag.views
"""

from django.conf.urls import url

from . import views

app_name = 'flag'
urlpatterns = [
    url(
        r'(?P<app_label>\w+)/(?P<object_name>\w+)/(?P<object_id>\d+)/$',
        views.confirm, name="flag_confirm"),
    url(r"^$", views.flag, name="flag_content"),
]
