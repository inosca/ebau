import json.decoder

import requests
from caluma.caluma_core.visibilities import BaseVisibility, filter_queryset_for
from caluma.caluma_form import models as form_models, schema as form_schema
from django.conf import settings
from django.db.models import Exists, F, OuterRef, Q

from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.utils import build_url, filters, headers


class CustomVisibility(BaseVisibility):
    """Custom visibility for Kanton Bern.

    This defers the visibility to CAMAC-NG, by querying the NG API for all
    visible instances for the given user.

    Note: This expects that each document has a meta property that stores the
    CAMAC instance identifier, named "camac-instance-id". Each node is
    filtered by indirectly looking for the value of said property.

    To avoid multiple lookups to the Camac-NG API, the result is cached in the
    request object, and resused if the need arises. Caching beyond a request is
    not done but might become a future optimisation.
    """

    @filter_queryset_for(form_schema.Document)
    def filter_queryset_for_document(self, node, queryset, info):
        return queryset.annotate(
            # This subquery checks if the family document (root document) is
            # accessible by rules of the CAMAC ACLs
            accessible=Exists(
                form_models.Document.objects.filter(
                    **{
                        "pk": OuterRef("family"),
                        "meta__camac-instance-id__in": self._all_visible_instances(
                            info
                        ),
                    }
                )
            )
        ).filter(
            # document is accessible through CAMAC ACLs
            Q(accessible=True)
            # OR dashboard documents
            | Q(form__slug=DASHBOARD_FORM_SLUG)
            # OR unlinked table documents created by the requesting user
            | Q(
                **{
                    "meta__camac-instance-id__isnull": True,
                    "family": F("pk"),
                    "created_by_user": info.context.user.username,
                }
            )
        )

    def _all_visible_instances(self, info):
        """Fetch visible camac instances from NG API, caches the result.

        Take user's group from a custom HTTP header named `X-CAMAC-GROUP`
        which is then forwarded as a filter to the NG API to retrieve all
        Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:
            return result

        resp = requests.get(
            build_url(settings.INTERNAL_BASE_URL, "/api/v1/instances"),
            # forward filters via query params
            {**filters(info), "fields[instances]": "id"},
            headers=headers(info),
        )

        try:
            jsondata = resp.json()
            if "error" in jsondata:
                # forward Instance API error to client
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            instance_ids = [int(rec["id"]) for rec in jsondata["data"]]

            setattr(info.context, "_visibility_instances_cache", instance_ids)

            return instance_ids

        except json.decoder.JSONDecodeError:
            raise RuntimeError("NG API returned non-JSON response, check configuration")

        except KeyError:
            raise RuntimeError(
                f"NG API returned unexpected data structure (no data key): {jsondata}"
            )
