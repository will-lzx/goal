from django.db import models

# Create your models here.


class Images(models.Model):
    history_id = models.IntegerField()
    headImg = models.FileField(upload_to='./upload/')
    create_time = models.DateField()


