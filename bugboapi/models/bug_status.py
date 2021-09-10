from django.db import models

class BugStatus(models.Model):

    name = models.CharField(max_length=25)