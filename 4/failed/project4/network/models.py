from django.views.generic import ListView
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timezone


class User(AbstractUser):
    following = models.ManyToManyField("self", related_name="followers")


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=256)
    likes = models.IntegerField(max_length=12, default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "author": self.author.username,
            "message": self.message,
            "likes": self.likes,
            "timestamp": self.timestamp
        }
    
