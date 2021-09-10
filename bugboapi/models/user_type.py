from django.db import models

class UserType(models.Model):

    name = models.CharField(max_length=25)
    description = models.CharField(max_length=100)