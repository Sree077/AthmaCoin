from django.contrib.auth.models import AbstractUser
from django.db import models

# class shopcode(models.Manager):
#     name = models.CharField()
#     code = models.IntegerField()
#     def __str__(self):
#         return f"{self.name} - {self.code}"
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    AthmaCoin = models.IntegerField(default=0)
    # claimedcodes = models.ManyToManyField(shopcode)

