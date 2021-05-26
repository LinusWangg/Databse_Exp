from django.db import models

# Create your models here.

class User(models.Model):
    user_act = models.CharField(max_length=255,unique=True,primary_key=True)
    user_pwd = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255,unique=True)
    user_birth = models.DateField(auto_now=True,null=False)
    user_avatar = models.CharField(max_length=255,null=True)
