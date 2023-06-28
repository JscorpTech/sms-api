from django.db import models

from accounts.models import User


class SmsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sms = models.TextField()
    phone = models.IntegerField()
