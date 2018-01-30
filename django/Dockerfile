FROM python:3.6

RUN apt-get update && apt-get install -y --no-install-recommends \
  ghostscript \
&& rm -rf /var/lib/apt/lists/* \
&& pip install uwsgi==2.0.15

ENV DJANGO_SETTINGS_MODULE camac.settings
ENV UWSGI_INI /app/uwsgi.ini
ENV DJANGO_DATABASE_PORT 5432

COPY . /app
WORKDIR /app

RUN make install \
&& find . -name "*.pyc" -delete

EXPOSE 80

CMD /bin/sh -c "./wait-for-it.sh $DJANGO_DATABASE_HOST:$DJANGO_DATABASE_PORT -- make install && ./manage.py migrate && uwsgi"
