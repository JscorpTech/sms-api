from django.urls import path

from api.views import SendSmsApi

app_name = "api"
urlpatterns = [
    path("send/", SendSmsApi.as_view(), name="send")
]
