import re
from django.db.models import Q
# from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from .models import Video
from .serializers import VideoSerializer


class VideoListAPIView(generics.ListAPIView):

    serializer_class = VideoSerializer
    pagination_class = LimitOffsetPagination
    queryset = Video.objects.all().order_by('-published_at')


class VideoSearchAPIView(generics.ListAPIView):

    serializer_class = VideoSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if 'search_term' in self.request.query_params:
            search_term = self.request.query_params['search_term']

            replace_chars = ['.', ',', '-', '[', ']', '/', '\\', ':', ';', "'", '"']
            for char in replace_chars:
                search_term = search_term.replace(char, '')
            search_term_trimmed = re.sub(' +', ' ', search_term.strip())

            # Get list of words to search for
            search_keywords = search_term_trimmed.split(' ')

            # Generate Query to match all words
            query = Q()
            for entry in search_keywords:
                query = query & (Q(title__icontains=entry) | Q(description__icontains=entry))

            return Video.objects.filter(query).order_by('-published_at')
        else:
            return Video.objects.none()
