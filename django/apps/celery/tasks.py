from celery.decorators import task
from datetime import datetime
from .fetch_videos import FetchVideos


@task(name='dummy_test_task')
def dummy_test_task():
    return 'Successfully executed at: {}(UTC)'.format(datetime.now())


@task(name="fetch_videos")
def fetch_videos():
    instance = FetchVideos()
    return instance.run()
