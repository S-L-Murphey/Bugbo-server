from django.db import models

class Bug(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    entry_date = models.DateField()
    creator = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='creator')
    status = models.ForeignKey("BugStatus", on_delete=models.CASCADE)
    priority = models.ForeignKey("BugPriority", on_delete=models.CASCADE)
    type = models.ForeignKey("BugType", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="BugTag")
    owner = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='owner')
