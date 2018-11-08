from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Users(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="用户ID")
    nickname = models.CharField(max_length=255, unique=True, default="普通用户", verbose_name="用户昵称")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    gender = models.CharField(max_length=10, default="女", verbose_name="用户性别")
    header_img = models.ImageField(upload_to="static/store/header", default="static/store/header/01.jpg", verbose_name="用户头像")
    phone = models.CharField(max_length=255, verbose_name="用户电话")
    address = models.CharField(max_length=255, verbose_name="用户地址")
    email = models.CharField(max_length=255, verbose_name="用户邮箱")
    Users = models.OneToOneField(User, on_delete=models.CASCADE)


