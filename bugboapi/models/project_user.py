from django.db import models

class ProjectUser(models.Model):

    user = models.ForeignKey("Employee", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)