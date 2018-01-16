FROM python:3.6

RUN apt-get update && apt-get install -y --no-install-recommends \
  ghostscript \
&& rm -rf /var/lib/apt/lists/* \
&& pip install uwsgi==2.0.15

ENV DJANGO_SETTINGS_MODULE camac.settings
ENV UWSGI_INI /app/uwsgi.ini

COPY . /app
WORKDIR /app

RUN make install

EXPOSE 80
CMD ["uwsgi"]
