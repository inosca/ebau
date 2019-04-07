FROM projectcaluma/caluma

ENV VISIBILITY_CLASSES caluma.core.visibilities.Any
ENV PERMISSION_CLASSES caluma.core.permissions.AllowAny
ENV LANGUAGE_CODE de
ENV LANGUAGES de
ENV OIDC_BEARER_TOKEN_REVALIDATION_TIME 300

COPY extensions /app/caluma/extensions
COPY fixtures /app/caluma/fixtures

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && ./manage.py loaddata caluma/fixtures/config.json && uwsgi"
