# Remember to update volume mounts for certificates in kt_uri-prod.yml when updating version
FROM python:3.8-slim

RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt-get update && apt-get install -y --no-install-recommends \
  git \
  build-essential \
  curl \
  entr \
  imagemagick \
  ghostscript \
  postgresql-client \
  gettext \
  locales \
  libreoffice \
  # manabi dependencies
  libsodium23=1.0.18-1 \
  # alexandria dependencies
  ffmpeg \
  inkscape \
  libfile-mimeinfo-perl \
  libimage-exiftool-perl \
  libjpeg-dev \
  libmagic1 \
  libsecret-1-0 \
  poppler-utils \
  webp \
  zlib1g-dev \
&& rm -rf /var/lib/apt/lists/*

RUN \
  # Create necessary folders
  mkdir /app \
  # Locale configuration
  && sed -i -e 's/# de_CH.UTF-8 UTF-8/de_CH.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && update-locale LANG=de_CH.UTF-8 \
  # Fix ImageMagick policy for creating thumbnails
  && sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read | write" pattern="PDF" \/>/' /etc/ImageMagick-6/policy.xml

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE camac.settings
ENV UWSGI_INI /app/uwsgi.ini
ENV DATABASE_PORT 5432

ARG REQUIREMENTS=requirements.txt
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --no-cache-dir --upgrade -r $REQUIREMENTS --disable-pip-version-check

COPY . /app

EXPOSE 80

CMD /bin/sh -c "./wait-for-it.sh $DATABASE_HOST:$DATABASE_PORT -- ./manage.py migrate && ./manage.py collectstatic --noinput && ./manage.py camac_load && uwsgi"
