from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    CLAIMED = 1
    UNCLAIMED = 0

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    status = models.IntegerField(choices=((UNCLAIMED, "not claimed"), (CLAIMED, "claimed")), default=UNCLAIMED)

    def __str__(self):
        return f"{self.code} | {self.status}"

    def is_claimed(self):
        return self.status == self.CLAIMED


class UserShop(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} | {self.shop.name}"
