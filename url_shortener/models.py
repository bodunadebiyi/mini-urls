from django.db import models
from django.contrib.auth.models import User

class Urls(models.Model):
    original_url = models.CharField(max_length=300)
    shortened_url = models.CharField(max_length=60)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_urls")
    hits = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
