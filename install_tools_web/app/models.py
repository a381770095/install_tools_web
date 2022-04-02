from django.db import models
# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone = models.BigIntegerField(verbose_name="手机号",null=True,blank=True)
    avatar = models.FileField(upload_to='avatar/',default='avata/default.jpg',verbose_name='用户头像')
    create_time = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "用户表"
    def __str__(self):
        return self.username



class Hosts(models.Model):
    host = models.CharField(verbose_name="IP",null=True,blank=True)
    port = models.CharField(verbose_name="端口",null=True,blank=True)
    username = models.CharField(verbose_name="用户名",null=True,blank=True)
    password = models.CharField(verbose_name="密码",null=True,blank=True)

    create_time = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "主机表"
    def __str__(self):
        return self.host



class Hosts(models.Model):
    host = models.CharField(verbose_name="IP",max_length=32)
    port = models.CharField(verbose_name="端口",max_length=32)
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)

    create_time = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "主机表"
    def __str__(self):
        return self.host




class Shells(models.Model):
    name = models.CharField(verbose_name="名称",max_length=32)
    path = models.FileField(upload_to='shellfile/',verbose_name='shell脚本')
    create_time = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "脚本表"
    def __str__(self):
        return self.name

