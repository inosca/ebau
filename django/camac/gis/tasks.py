from celery import shared_task
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from camac.gis.models import GISDataSource
from camac.gis.utils import merge_data


def _get_client(gis_data: str):
    # Indirection for better testability - this can get mocked
    # in tests
    return import_string(gis_data.client)


def schedule_process_gis_data_sources(queryset, query_params):
    # Run validation before scheduling actual processing

    client_ids = []

    for gis_data in queryset:
        try:
            for required_param in gis_data.get_required_params():
                if required_param not in query_params.keys():
                    raise ValueError(
                        _("Required parameter %(parameter)s was not passed")
                        % {"parameter": required_param}
                    )

            client_ids.append(gis_data.pk)

        except ValueError as e:
            raise ValidationError(e)

    # TODO: somehow pass aloing the "gis" group that django-q used.
    # I guess this should be used as a queue identifier (or whatever the
    # meaning of "group" was in django-q)
    return process_gis_data_sources.delay(client_ids, query_params)  # noqa: SG001


@shared_task
def process_gis_data_sources(data_source_ids, query_params):
    """Process data sources.

    Private - you should use the schedule_process_gis_data_sources()
    function instead!
    """

    queryset = GISDataSource.objects.filter(
        disabled=False, pk__in=data_source_ids
    ).order_by("sort")

    data = {}
    errors = []

    for gis_data in queryset:
        # Validation happened in schedule_process_gis_data_sources(), so
        # not doing that again here. We just have to assume things work
        try:
            client = _get_client(gis_data)(query_params)
            new_data = client.process_data_source(gis_data.config, data)

            merge_data(data, new_data, client.merge_strategy)

        except RuntimeError as e:
            errors.append(
                {
                    "detail": str(e),
                    "client": gis_data.client,
                    "data_source_id": gis_data.pk,
                    "data_source_description": gis_data.description,
                }
            )
    return data, errors
