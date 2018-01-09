FROM python:3.6

RUN pip install uwsgi==2.0.15

ENV DJANGO_SETTINGS_MODULE camac.settings
ENV UWSGI_INI /app/uwsgi.ini

COPY . /app
WORKDIR /app

RUN make install

EXPOSE 80
CMD ["uwsgi"]
