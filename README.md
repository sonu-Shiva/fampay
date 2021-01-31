# Install Docker

# Project Setup

1.fork, clone and navigate into this repository

   `git clone https://github.com/sonu-Shiva/fampay.git`

2.Build docker (Check if docker is up and running):

   `docker-compose up --build -d`

3.Create super user:

   `docker-compose exec -u root django bash`

   `python manage.py createsuperuser`

4.The backend server will always be available at `localhost:8000`

5.Manually Running server:

   `docker-compose exec -u root django bash`

   `python manage.py migrate`

   `python manage.py runserver 0:8000`

# Adding Api Keys

1.Make a POST call on `http://localhost:8000/add-api-keys/` with payload `{'api_keys': ["<api_key1>", "<api_key2>", ...]}`

# Running async job for fetching videos

1.Login to admin panel at `http://localhost:8000/admin`

2.Click on `Periodic Tasks`

3.Click on `Add Periodic Task`

4.Give some name to the taks and select the `fetch_videos` job in the Task(registered) dropdown.

5.Make sure the `Enabled` checkbox is checked.

6.Under `Schedule` > `Interval Schedule` > click on `+(add)` button and create a schedule of 10seconds and save.

7.Finally save the periodic task.

# Checking logs

1.You can check the logs of the jobs running on celery by executing the command `docker-compose logs -f celery`

2.You can check the logs of celery scheduler by executing the command `docker-compose logs -f celery-beat`

3.You can check the logs of server by executing the command `docker-compose logs -f django`

# Videos Listing API

1.Videos Listing Api endpoint: `GET` `http://localhost:8000/videos/`

2.Params: `limit`, `offset`

# Search API

1.`Cricket` is the query used for fetching and storing videos data from youtube.

2.Videos Listing Api endpoint: `GET` `http://localhost:8000/videos/search/`

3.Params: `search_term`, `limit`, `offset`
