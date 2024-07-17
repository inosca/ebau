FROM ghcr.io/adfinis/document-merge-service:7.0.0

# Only root user can install packages
USER root
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends hyphen-de hyphen-fr
USER document-merge-service

RUN poetry run pip install boto3==1.34.117

ENV CACHE_BACKEND=django.core.cache.backends.memcached.PyMemcacheCache
ENV DATABASE_ENGINE=django.db.backends.postgresql
ENV REQUIRE_AUTHENTICATION=True
ENV PAGINATION_ENABLED=False
ENV DMS_VISIBILITY_CLASSES=document_merge_service.extensions.visibilities.CustomVisibility
ENV DMS_PERMISSION_CLASSES=document_merge_service.extensions.permissions.CustomPermission

ARG APPLICATION

COPY Makefile .
COPY uwsgi.ini .
COPY fonts /usr/local/share/fonts
COPY extensions document_merge_service/extensions
COPY $APPLICATION /tmp/document-merge-service/

CMD /bin/sh -c "poetry run python ./manage.py migrate \
  && poetry run python manage.py loaddata /tmp/document-merge-service/dump.json \
  && poetry run python manage.py upload_local_templates -s '/tmp/document-merge-service/templatefiles/*.docx' \
  && poetry run uwsgi"
