from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_summernote.fields import SummernoteTextField


class Documents(models.Model):
    title = models.CharField(max_length=300)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Entries"

class BlogPost(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = SummernoteTextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title