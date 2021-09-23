from django.db import models
from django.contrib.auth.models import User #pylint: disable=imported-auth-user

class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    avatar = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    user_type = models.ForeignKey("UserType", on_delete=models.CASCADE)