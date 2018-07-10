import datetime
from django.db import models

# Create your models here.


class Images(models.Model):
    history_id = models.IntegerField()
    headImg = models.FileField(upload_to='./upload/')
    create_time = models.DateField()


class Goal(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    goal_type = models.IntegerField()
    frequent = models.IntegerField()
    frequent_value = models.IntegerField()
    period = models.IntegerField()
    status = models.IntegerField(default=0)
    goal_value = models.FloatField()
    author = models.CharField(max_length=150)
    createtime = models.DateTimeField(default=datetime.datetime.now())
    updatetime = models.DateTimeField(auto_now=True)


class Intendance(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    goal_id = models.IntegerField()
    intendancer = models.CharField(max_length=150)
    intendance_value = models.FloatField()
    createtime = models.DateTimeField(default=datetime.datetime.now())
    updatetime = models.DateTimeField(auto_now=True)


class History(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    goal_id = models.IntegerField()
    image = models.BinaryField()
    # 统一为分钟
    time_long = models.IntegerField()
    time_quantity = models.CharField(max_length=100)
    createtime = models.DateTimeField(default=datetime.datetime.now())
    updatetime = models.DateTimeField(auto_now=True)






