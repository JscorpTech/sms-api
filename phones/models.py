from django.db import models

from accounts.models import User


class Phones(models.Model):
    phone = models.IntegerField(max_length=12)
    token = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.phone)
