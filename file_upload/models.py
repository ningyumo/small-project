from django.db import models
import uuid
from user.models import UserProfile
import os


def user_directory_path(instance, filename):
    file_type = filename.split(".")[-1]
    filename = "{0}.{1}".format(uuid.uuid4().hex[:10], file_type)
    return os.path.join("files", file_type, filename)


class File(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)
    created_time = models.DateTimeField(auto_now_add=True)


