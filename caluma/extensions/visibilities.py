import json.decoder
import os
import urllib.parse
from logging import getLogger

import requests

from caluma.core.visibilities import BaseVisibility, filter_queryset_for
from caluma.form import models as form_models, schema as form_schema

log = getLogger()

"""Caluma visibilities for Kanton Bern"""


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


def accessible_doc_families(info):
    """Return all accessible form family IDs for the current user.

    Note, this only works for role "gesuchsteller". It will find all
    document family IDs that contain an answer with the request user in the
    "gesuchsteller" list.
    """

    user_identifier = info.context.user.userinfo.get("sub")
    user_email = info.context.user.userinfo.get("email")

    """
    Warning: This feature has been temporarily disabled, because it caused
    "lock-out" issues during testing. The "invite" feature still needs to be
    clearly specified and implemented accordingly.
    """
    # Find documents where I'm registered as a requester ("gesuchsteller").
    docs_requester = form_models.Document.objects.filter(
        family__in=form_models.Answer.objects.filter(
            question_id="e-mail-gesuchstellerin____disabled", value=user_email
        ).values("document__family")
    )

    # Find documents that I've created, but exclude all documents that have
    # at least one requester email configured.  Those MUST be matched via
    # user email, it is not relevant anymore if the current user has once
    # created it.
    docs_creator = form_models.Document.objects.filter(
        created_by_user=user_identifier
    ).exclude(
        family__in=form_models.Answer.objects.filter(
            question_id="e-mail-gesuchstellerin____disabled"
        ).values("document__family")
    )

    # combine the result sets, and extract the family. From here on, we
    # use the family IDs instead of document IDs, so we don't have to worry
    # about nesting when calculating access.
    return (docs_creator | docs_requester).values("family")


class FilterViaCamacAPIMixin:
    """Mixin to make the actual visibility class more readable."""

    def filter_qs(self, qs, info):
        """Filter given queryset by answer pointing to camac instances.

        We implement ACL by having a question/answer that stores the CAMAC
        Instance identifier. Then for each access, we query CAMAC to see which
        instances we're allowed to see.

        This takes the given queryset, filters it to only contain objects that
        contain answers referring to the set of camac instance ids that we're
        allowed to access.
        """

        filter_dict = self._filter_dict_for(info, qs.model.__name__)
        log.debug(f"filtering for model {qs.model.__name__}: {filter_dict}")
        return qs.filter(**filter_dict)

    def _filter_dict_for(self, info, qs_model):
        """Return a filter function for the given queryset model.

        Returns a lambda function that filters a queryset according to the
        user's role and queryset type.
        """

        # QS model -> user role -> (lambda -> filter dict)
        #
        # We only want to generate the filter dict on-demand, as it may involve
        # calling out to the NG API or doing other calculations etc
        filters_by_model_and_role = {
            "Document": {
                "gesuchsteller": lambda: dict(
                    # Same special case again
                    family__in=accessible_doc_families(info)
                ),
                "_default": lambda: {
                    "family__in": form_models.Document.objects.filter(
                        **{
                            "meta__camac-instance-id__in": self._all_visible_instances(
                                info
                            )
                        }
                    ).values("pk")
                },
            },
            "Answer": {
                "gesuchsteller": lambda: dict(
                    # Same special case again, this time indirectly via document
                    document__family__in=accessible_doc_families(info)
                ),
                "_default": lambda: dict(
                    # Instance question is in top-level document
                    document__family__in=form_models.Document.objects.filter(
                        **{
                            "meta__camac-instance-id__in": self._all_visible_instances(
                                info
                            )
                        }
                    ).values("pk")
                ),
            },
        }

        if qs_model not in filters_by_model_and_role:
            raise RuntimeError(
                "Requested model %s has no configured visibility" % qs_model
            )
        default_filter = filters_by_model_and_role[qs_model]["_default"]

        filter_func = filters_by_model_and_role[qs_model].get(
            role(info), default_filter
        )
        return filter_func()

    def _all_visible_instances(self, info):
        """Fetch visible camac instances from NG API, caches the result.

        Take user's role from a custom HTTP header named `X-CAMAC-Role`. If
        it's not given, defaults to "gesuchsteller".

        The role is then forwarded as a filter to the NG API to retrieve all
        Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:
            return result

        camac_api = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")

        resp = requests.get(
            f"{camac_api}/api/v1/instances",
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


class CustomVisibility(BaseVisibility, FilterViaCamacAPIMixin):
    """Custom visibility for Kanton Bern.

    This defers the visibility to CAMAC-NG, by querying the NG API for all
    visible instances for the given user.

    Note: This expects that each form has a question that stores the CAMAC
    instance identifier, named "camac-instance-id". Each node is filtered by
    indirectly looking for an answer to that question.

    To avoid multiple lookups to the Camac-NG API, the result is cached in the
    request object, and resused if the need arises. Caching beyond a request is
    not done but might become a future optimisation.
    """

    def make_filter_method(node_type):
        """Return a filter method for the given node type.

        Note, this must be called at class-declaration time. At runtime, this
        will not do what expected.

        TODO: A future improvement would probably be to cache the already
        filtered records (or their PKs) per node, and use them for followup
        lookups within the same request, thus easing database load by reducing
        the number of JOINs this generates.
        """

        @filter_queryset_for(node_type)
        def method(self, node, queryset, info):
            return self.filter_qs(queryset, info)

        return method

    document = make_filter_method(form_schema.Document)
    answer = make_filter_method(form_schema.Answer)

    # no use in keeping that helper at runtime (would only be turned into a
    # method that nobody can use)
    del make_filter_method
