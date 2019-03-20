FROM projectcaluma/caluma

ENV VISIBILITY_CLASSES caluma.extensions.visibilities.CustomVisibility
ENV PERMISSION_CLASSES caluma.extensions.permissions.CustomPermission
ENV VALIDATION_CLASSES caluma.extensions.validations.CustomValidation

ENV LANGUAGE_CODE de
ENV LANGUAGES de
ENV OIDC_BEARER_TOKEN_REVALIDATION_TIME 300

COPY extensions /app/caluma/extensions
COPY fixtures /app/caluma/fixtures

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && ./manage.py loaddata caluma/fixtures/config.json && uwsgi"
