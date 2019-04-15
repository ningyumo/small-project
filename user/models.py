from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    nick_name = models.CharField(max_length=10, unique=True, blank=True)
    tel = models.BigIntegerField(unique=True)
    sex = models.CharField(max_length=10, choices=gender)
    created_time = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nick_name
