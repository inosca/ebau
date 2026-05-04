FROM ghcr.io/adfinis/document-merge-service:9.2.1

# Only root user can install packages
USER root
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends hyphen-de hyphen-fr
USER document-merge-service

ENV CACHE_BACKEND=django.core.cache.backends.memcached.PyMemcacheCache
# https://pymemcache.readthedocs.io/en/latest/apidoc/pymemcache.client.base.html
ENV CACHE_OPTIONS=connect_timeout=0.1,timeout=0.1,no_delay=True,ignore_exc=True
ENV DATABASE_ENGINE=django.db.backends.postgresql
ENV REQUIRE_AUTHENTICATION=True
ENV PAGINATION_ENABLED=False
ENV DMS_VISIBILITY_CLASSES=document_merge_service.extensions.visibilities.CustomVisibility
ENV DMS_PERMISSION_CLASSES=document_merge_service.extensions.permissions.CustomPermission
ENV DATA_UPLOAD_MAX_NUMBER_FIELDS=2000

# We will migrate to a startup task in K8s soon, this is
# just in preparation for it
ENV MIGRATE_ON_STARTUP=true
ENV LOAD_TEMPLATES_ON_STARTUP=true
ENV DISABLE_WEB_SERVICE=false

ARG APPLICATION

COPY Makefile .
COPY fonts /usr/local/share/fonts
COPY extensions document_merge_service/extensions
COPY $APPLICATION /tmp/document-merge-service/

COPY entrypoint.sh /app/

CMD ["gunicorn"]
ENTRYPOINT ["/app/entrypoint.sh"]
