FROM ghcr.io/adfinis/document-merge-service:6.4.0

# Only root user can install packages
USER root
RUN poetry run pip install boto3==1.28.9
USER document-merge-service

ENV CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
ENV DATABASE_ENGINE=django.db.backends.postgresql
ENV REQUIRE_AUTHENTICATION=True
ENV PAGINATION_ENABLED=False
ENV DMS_VISIBILITY_CLASSES=document_merge_service.extensions.visibilities.CustomVisibility
ENV DMS_PERMISSION_CLASSES=document_merge_service.extensions.permissions.CustomPermission

COPY Makefile .
COPY uwsgi.ini .
COPY fonts /usr/local/share/fonts
COPY extensions document_merge_service/extensions
