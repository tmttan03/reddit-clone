from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.title)