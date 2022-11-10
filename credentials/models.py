from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=30,null=True)
    branch = models.CharField(max_length=30,null=True)
    role = models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.user.username

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingDate = models.CharField(max_length=30,null=True)
    branch =  models.CharField(max_length=30,null=True)
    subject =  models.CharField(max_length=30,null=True)
    notesFile = models.FileField(max_length=30,null=True)
    fileType =  models.CharField(max_length=30,null=True)
    description =  models.CharField(max_length=30,null=True)
    status = models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.user.username+ " "+ self.status 