# Remember to update volume mounts for certificates in kt_uri-prod.yml when updating version
FROM python:3.10-slim

# Needs to be set for users with manually set UID
ENV HOME=/home/ebau

ENV APP_HOME=/app
ENV DJANGO_SETTINGS_MODULE=camac.settings
ENV UWSGI_INI=$APP_HOME/uwsgi.ini
ENV DATABASE_PORT=5432
ENV STATIC_DIR=$APP_HOME/staticfiles

RUN mkdir -p $APP_HOME $STATIC_DIR \
    && useradd -u 901 -r ebau --create-home \
    # All project specific folders need to be accessible by newly created user
    # but also for unknown users (when UID is set manually). Such users are in
    # group root.
    && chown -R ebau:root $HOME $STATIC_DIR \
    && chmod -R 770 $HOME $STATIC_DIR

RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
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
  wait-for-it \
  zlib1g-dev \
&& rm -rf /var/lib/apt/lists/*

RUN \
  # Locale configuration
  sed -i -e 's/# de_CH.UTF-8 UTF-8/de_CH.UTF-8 UTF-8/' /etc/locale.gen \
  && dpkg-reconfigure --frontend=noninteractive locales \
  && update-locale LANG=de_CH.UTF-8 \
  # Fix ImageMagick policy for creating thumbnails
  && sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read | write" pattern="PDF" \/>/' /etc/ImageMagick-6/policy.xml

WORKDIR $APP_HOME

ARG REQUIREMENTS=requirements.txt
COPY requirements.txt requirements-dev.txt $APP_HOME/
# TODO: Remove --no-build-isolation as soon as https://github.com/pypa/setuptools/issues/4519 is fixed!
RUN pip install --no-cache-dir --upgrade -r $REQUIREMENTS --no-build-isolation

COPY . $APP_HOME

EXPOSE 80

CMD /bin/sh -c "wait-for-it $DATABASE_HOST:$DATABASE_PORT -- ./manage.py migrate && ./manage.py collectstatic --noinput && ./manage.py camac_load && uwsgi"
