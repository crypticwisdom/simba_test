from random import random

from django.db import models
from uuid import uuid4

# Create your models here.


class Identifier(models.Model):
    """
        Since there's no Registration / Login System in this Application.
        Users of this App. should create any TASK with his/her email address,
        For them to be able to list and recognize their own task.
        ...
        This model holds email addresses of users.
        This model will be extended by the `Task` Model
    """
    email = models.EmailField(unique=True)

    def __str__(self):
        return str(self.email)


class Task(models.Model):
    """
        Extend the `Identifier` Model.
    """

    STATUS = (
        ("Open", "OPEN"),
        ("Completed", "COMPLETED")
    )

    email = models.ForeignKey(Identifier, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, default="")
    slug = models.SlugField(max_length=30, null=False, blank=False)
    state = models.CharField(max_length=9, default="open", choices=STATUS)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

