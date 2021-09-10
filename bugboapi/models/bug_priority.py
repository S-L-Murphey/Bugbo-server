from django.db import models

class BugPriority(models.Model):

    label = models.CharField(max_length=25)