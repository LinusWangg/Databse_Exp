from django.db import models
from django.db.models.fields import DateField

# Create your models here.

class Article(models.Model):
    art_title = models.CharField(max_length=255,unique=True,primary_key=True,null=False)
    art_content = models.CharField(max_length=1023)
    art_author = models.CharField(max_length=255,null=False)
    art_time = models.DateField(auto_now=True,null=False)
    art_type = models.IntegerField()

class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    art_title = models.CharField(max_length=255)
    commentor = models.CharField(max_length=255)
    commentwho = models.IntegerField(default=0)
    comment_content = models.CharField(max_length=127)
    comment_time = DateField(auto_now=True,null=False)
