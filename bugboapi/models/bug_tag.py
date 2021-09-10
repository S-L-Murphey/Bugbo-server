from django.db import models

class BugTag(models.Model):

    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    bug = models.ForeignKey("Bug", on_delete=models.CASCADE)