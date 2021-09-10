from django.db import models

class Bug(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    entry_date = models.DateField
    creator = models.ForeignKey("Employee", on_delete=models.CASCADE)
    status = models.ForeignKey("BugStatus", on_delete=models.CASCADE)