from django.db import models

class BugType(models.Model):

    label = models.CharField(max_length=15)