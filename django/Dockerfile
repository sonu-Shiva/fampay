FROM python:3.6.6
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
RUN ["apt-get", "install", "-y", "nano"]

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app
RUN chown -R root /app

RUN mkdir -p logs
RUN chown -R root /logs

RUN mkdir -p /app/media
RUN chown -R root /app/media

COPY ./entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && chown root /entrypoint.sh

WORKDIR /app

EXPOSE 6000
ENTRYPOINT ["/entrypoint.sh"]
