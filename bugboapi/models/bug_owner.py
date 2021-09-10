from django.db import models

class BugOwner(models.Model):

    user = models.ForeignKey("Employee", on_delete=models.CASCADE)
    bug = models.ForeignKey("Bug", on_delete=models.CASCADE)