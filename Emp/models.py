from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=45)
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    passwd = models.CharField(max_length=8)