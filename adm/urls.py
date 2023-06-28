from django.urls import path

from adm.views import HomePage

app_name = "adm"

urlpatterns = [
    path("", HomePage.as_view(), name="home")
]
