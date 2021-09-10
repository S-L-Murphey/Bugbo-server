from django.db import models

class BugProject(models.Model):

    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    bug = models.ForeignKey("Bug", on_delete=models.CASCADE)