import logging
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from apps.videos.models import ApiKey, Video


logger = logging.getLogger('application')


class FetchVideos(object):

    def __init__(self):
        pass

    @staticmethod
    def get_working_api_key(limit_exceeded_api_key=None):
        if limit_exceeded_api_key:
            logger.info('Quota exceeded for api_key {}'.format(limit_exceeded_api_key))
            ApiKey.objects.filter(api_key=limit_exceeded_api_key).update(limit_exceeded=True, limit_exceeded_on=datetime.now())

        api_key = None
        try:
            obj = ApiKey.objects.filter(limit_exceeded=False).first()
            api_key = obj.api_key
        except AttributeError:
            # trying to reuse api_keys that exceeded quota 5minutes ago
            five_minutes_ago = datetime.now() - relativedelta(minutes=5)
            objs = ApiKey.objects.filter(limit_exceeded=True, limit_exceeded_on__lte=five_minutes_ago).order_by('limit_exceeded_on')
            if objs.count():
                api_key = objs.first().api_key
                objs.update(limit_exceeded=False, limit_exceeded_on=None)

        if not api_key:
            logger.info('Quota exceeded on all avaialable api_keys')
        return api_key

    @staticmethod
    def get_response(api_key):
        api = 'https://www.googleapis.com/youtube/v3/search'
        published_after = datetime.now() - relativedelta(hours=2)
        params = {
            'key': api_key,
            'type': 'video',
            'order': 'date',
            'publishedAfter': published_after.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'part': 'snippet',
            'relevanceLanguage': 'en',
            'maxResults': 50,
            'q': 'cricket'
        }
        response = requests.request('GET', api, params=params)
        return response

    def run(self):
        try:
            api_key = self.get_working_api_key()
            if not api_key:
                raise Exception('Usable Api Key currently unavailable!')

            response = self.get_response(api_key)
            status_code = response.status_code
            if status_code == 200:
                data = response.json()
                videos_map = {}
                for item in data.get('items', []):
                    try:
                        snippet = item['snippet']
                        video_id = item['id']['videoId']
                        published_at = parse(snippet['publishedAt'])
                        obj = Video(**{
                            'video_id': video_id,
                            'channel_id': snippet['channelId'],
                            'title': snippet['title'],
                            'description': snippet['description'],
                            'published_at': published_at,
                            'thumbnail_default': snippet['thumbnails']['default']['url'],
                            'thumbnail_medium': snippet['thumbnails']['medium']['url'],
                            'thumbnail_high': snippet['thumbnails']['high']['url'],
                        })
                        videos_map[video_id] = obj
                    except KeyError as e:
                        logger.info('Skipping an item due to KeyError({})'.format(e))

                video_ids = list(videos_map.keys())
                existing_videos = list(Video.objects.filter(video_id__in=video_ids).values_list('video_id', flat=True))
                if existing_videos:
                    logger.error('Found {} existing videos.'.format(len(existing_videos)))
                for video_id in existing_videos:
                    del videos_map[video_id]

                if videos_map:
                    videos = list(videos_map.values())
                    logger.info('Inserting {} new videos.'.format(len(videos)))
                    Video.objects.bulk_create(videos)
            elif status_code == 403:
                logger.error('[Response StatusCode: {}] {}'.format(status_code, response.json()))
                error_data = response.json()
                for error in error_data['error']['errors']:
                    if error['reason'] == 'quotaExceeded':
                        self.get_working_api_key(api_key)
            else:
                logger.error('[Response StatusCode: {}] {}'.format(status_code, response.json()))
        except Exception as e:
            logger.error('[Unhandled Exception] {}'.format(e))
