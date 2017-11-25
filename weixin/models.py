from django.db import models
from django import forms

# Create your models here.


class Images(models.Model):
    history_id = models.IntegerField()
    headImg = models.FileField(upload_to='./upload/')
    create_time = models.DateField()


class UploadFileForm(forms.Form):
    index = forms.IntegerField()
    file = forms.FileField()


