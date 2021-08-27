from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Content_Item(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_accessed = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Content(models.Model):
    source_title = models.CharField(max_length=100)
    source_url = models.TextField()
    topics = models.TextField()
    text = models.TextField()
    images = models.TextField()

    def __str__(self):
        return self.topics
