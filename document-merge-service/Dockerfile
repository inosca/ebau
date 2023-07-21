FROM ghcr.io/adfinis/document-merge-service:6.3.0

ENV CACHE_BACKEND=django.core.cache.backends.memcached.MemcachedCache
ENV DATABASE_ENGINE=django.db.backends.postgresql
ENV REQUIRE_AUTHENTICATION=True
ENV PAGINATION_ENABLED=False
ENV DMS_VISIBILITY_CLASSES=document_merge_service.extensions.visibilities.CustomVisibility
ENV DMS_PERMISSION_CLASSES=document_merge_service.extensions.permissions.CustomPermission

COPY Makefile .
COPY uwsgi.ini .
COPY extensions document_merge_service/extensions
