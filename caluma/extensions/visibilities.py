import json.decoder
import os
import urllib.parse

import requests

from caluma.core.visibilities import BaseVisibility, filter_queryset_for
from caluma.form import models as form_models, schema as form_schema


CAMAC_NG_URL = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")


def role(info):
    """Extract role name from request."""
    return info.context.META.get("HTTP_X_CAMAC_ROLE", "gesuchsteller")


def filters(info):
    """Extract Camac NG filters from request.

    The filters are expected to be a URLencoded string (foo=bar&baz=blah).
    """
    return dict(
        urllib.parse.parse_qsl(info.context.META.get("HTTP_X_CAMAC_FILTERS", ""))
    )


def group(info):
    """Extract group name from request."""
    return info.context.META.get("HTTP_X_CAMAC_GROUP", None)


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
        return queryset.filter(family__in=self._all_visible_documents(info))

    @filter_queryset_for(form_schema.Answer)
    def filter_queryset_for_answer(self, node, queryset, info):
        return queryset.filter(document__family__in=self._all_visible_documents(info))

    def _all_visible_documents(self, info):
        """Fetch all visible caluma documents and cache the result. """

        result = getattr(info.context, "_visibility_documents_cache", None)
        if result is not None:
            return result

        document_ids = form_models.Document.objects.filter(
            **{"meta__camac-instance-id__in": self._all_visible_instances(info)}
        ).values_list("pk", flat=True)

        setattr(info.context, "_visibility_documents_cache", document_ids)

        return document_ids

    def _all_visible_instances(self, info):
        """Fetch visible camac instances from NG API, caches the result.

        Take user's role from a custom HTTP header named `X-CAMAC-ROLE`. If
        it's not given, defaults to "gesuchsteller".

        The role is then forwarded as a filter to the NG API to retrieve all
        Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:
            return result

        resp = requests.get(
            f"{CAMAC_NG_URL}/api/v1/instances",
            # forward filters, role and group via query params
            {
                **filters(info),
                "role": role(info),
                "group": group(info),
                "fields[instances]": "id",
            },
            # Forward authorization header
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        try:
            jsondata = resp.json()
            if "error" in jsondata:
                # forward Instance API error to client
                raise RuntimeError("Error from NG API: %s" % jsondata["error"])

            instance_ids = [int(rec["id"]) for rec in jsondata["data"]]
            setattr(info.context, "_visibility_instances_cache", instance_ids)

            return getattr(info.context, "_visibility_instances_cache")

        except json.decoder.JSONDecodeError:
            raise RuntimeError("NG API returned non-JSON response, check configuration")

        except KeyError:
            raise RuntimeError(
                "NG API returned unexpected data structure (no data key)"
            )
