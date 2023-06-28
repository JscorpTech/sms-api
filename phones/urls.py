from django.urls import path

from phones.views import SendSmsPage, VerifyPage, ListPage

app_name = "phone"

urlpatterns = [
    path("", ListPage.as_view(), name="list"),
    path("send-sms/", SendSmsPage.as_view(), name="send-sms"),
    path("verify/", VerifyPage.as_view(), name="verify"),
]
