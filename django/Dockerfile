FROM python:3.7

RUN apt-get update && apt-get install -y --no-install-recommends \
	ghostscript \
	postgresql-client \
	gettext \
	locales \
	libreoffice \
&& rm -rf /var/lib/apt/lists/* \
&& mkdir /app \
&& sed -i -e 's/# de_CH.UTF-8 UTF-8/de_CH.UTF-8 UTF-8/' /etc/locale.gen \
&& dpkg-reconfigure --frontend=noninteractive locales \
&& update-locale LANG=de_CH.UTF-8

# fix ImageMagick policy for creating thumbnails
RUN sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read | write" pattern="PDF" \/>/' /etc/ImageMagick-6/policy.xml

# install libsodium from source to make sure it's the same version as in production
RUN curl -LO https://download.libsodium.org/libsodium/releases/libsodium-1.0.18-stable.tar.gz \
&& tar xfv libsodium-1.0.18-stable.tar.gz \
&& cd libsodium-stable \
&& ./configure \
&& make \
&& make check \
&& make install \
&& ldconfig

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE camac.settings
ENV UWSGI_INI /app/uwsgi.ini
ENV DATABASE_PORT 5432

ARG REQUIREMENTS=requirements.txt
COPY requirements.txt requirements-dev.txt /app/

RUN pip install --no-cache-dir --upgrade -r $REQUIREMENTS  --disable-pip-version-check

COPY . /app

EXPOSE 80

CMD /bin/sh -c "./wait-for-it.sh $DATABASE_HOST:$DATABASE_PORT -- ./manage.py migrate && ./manage.py collectstatic --noinput && ./manage.py camac_load && uwsgi"
