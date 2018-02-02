FROM python:3.6

RUN apt-get update && apt-get install -y --no-install-recommends \
  ghostscript \
&& rm -rf /var/lib/apt/lists/* \
&& pip install uwsgi==2.0.15 \
&& mkdir /app

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE camac.settings
ENV UWSGI_INI /app/uwsgi.ini
ENV DJANGO_DATABASE_PORT 5432

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD /bin/sh -c "./wait-for-it.sh $DJANGO_DATABASE_HOST:$DJANGO_DATABASE_PORT --timeout=60 -- make install && ./manage.py migrate && ./manage.py loadconfig && uwsgi"
