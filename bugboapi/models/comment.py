from django.db import models

class Comment(models.Model):

    bug = models.ForeignKey("Bug", on_delete=models.CASCADE)
    commentor = models.ForeignKey("Employee", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    