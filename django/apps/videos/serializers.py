from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = Video
        exclude = []
        read_only_fields = ('video_id', 'channel_id', 'title', 'description', 'published_at')
