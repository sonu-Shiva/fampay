from django.db import models

# Create your models here.


class ApiKey(models.Model):
    api_key = models.CharField(max_length=255, unique=True)
    limit_exceeded = models.BooleanField(default=False)
    limit_exceeded_on = models.DateTimeField(null=True, blank=True)


class Video(models.Model):
    video_id = models.CharField(max_length=255, unique=True, db_index=True)
    channel_id = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField(db_index=True)
    thumbnail_default = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_medium = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_high = models.CharField(max_length=255, null=True, blank=True)
