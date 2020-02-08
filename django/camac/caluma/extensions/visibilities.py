from base64 import b64decode
from json import loads

from caluma.caluma_core.visibilities import BaseVisibility, filter_queryset_for
from caluma.caluma_form import models as form_models, schema as form_schema
from django.db.models import F, OuterRef, Q, Subquery

from camac.constants.kt_bern import DASHBOARD_FORM_SLUG
from camac.instance.filters import CalumaInstanceFilterSet
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.user.middleware import get_group
from camac.user.models import User
from camac.utils import filters


class CustomVisibility(BaseVisibility, InstanceQuerysetMixin):
    """Custom visibility for Kanton Bern.

    Note: This expects that each document has a meta property that stores the
    CAMAC instance identifier, named "camac-instance-id". Each node is
    filtered by indirectly looking for the value of said property.

    To avoid multiple db lookups, the result is cached in the
    request object, and reused if the need arises. Caching beyond a request is
    not done but might become a future optimisation.
    """

    instance_field = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = None
        self.user = None

    @filter_queryset_for(form_schema.Document)
    def filter_queryset_for_document(self, node, queryset, info):
        instance_ids = self._all_visible_instances(info)

        return queryset.annotate(
            # This subquery selects the meta property "camac-instance-id" which
            # holds the ID of the camac instance. This will be used to make
            # sure the CAMAC ACLs allow visibility of this document
            instance_id=Subquery(
                form_models.Document.objects.filter(pk=OuterRef("family")).values(
                    "meta__camac-instance-id"
                )[:1]
            )
        ).filter(
            # document is accessible through CAMAC ACLs
            Q(instance_id__in=instance_ids)
            # OR dashboard documents
            | Q(form_id=DASHBOARD_FORM_SLUG)
            # OR unlinked table documents created by the requesting user
            | Q(
                **{
                    "meta__camac-instance-id__isnull": True,
                    "family": F("pk"),
                    "created_by_user": info.context.user.username,
                }
            )
        )

    def get_base_queryset(self):
        """Overridden from InstanceQuerysetMixin to avoid the super().get_queryset() call."""
        instance_state_expr = self._get_instance_filter_expr("instance_state")
        return Instance.objects.all().select_related(instance_state_expr)

    def _parse_token(self, token):
        data = token.split(b".")[1]
        data += b"=" * (-len(data) % 4)

        return loads(b64decode(data))

    def _get_camac_user(self, oidc_user):
        # TODO: This is an ugly hack. It needs to be changed as soon as
        #  https://github.com/projectcaluma/caluma/issues/912 is fixed or we finally
        #  get rid of the request here.
        for username in [
            oidc_user.username,
            oidc_user.userinfo.get("preferred_username"),
        ]:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                continue

    def _enrich_request(self, info):
        oidc_user = info.context.user
        camac_user = self._get_camac_user(oidc_user)

        info.context.user = camac_user
        info.context.auth = self._parse_token(oidc_user.token)

        camac_group = get_group(info.context)
        info.context.group = camac_group
        info.context.oidc_user = oidc_user

        self.user = camac_user
        self.group = camac_group

    def _reset_request(self, info):
        info.context.user = info.context.oidc_user

        del info.context.auth
        del info.context.group
        del info.context.oidc_user

    def _all_visible_instances(self, info):
        """Fetch visible camac instances and cache the result.

        Take user's group from a custom HTTP header named `X-CAMAC-GROUP` or use
        default group  to retrieve all Camac instance IDs that are accessible.

        Return a list of instance identifiers.
        """
        result = getattr(info.context, "_visibility_instances_cache", None)
        if result is not None:  # pragma: no cover
            return result

        self._enrich_request(info)

        if not self.user:
            self._reset_request(info)
            return Instance.objects.none()

        filtered = CalumaInstanceFilterSet(
            data=filters(info),
            queryset=self.get_queryset(self.group),
            request=info.context,
        )

        instance_ids = list(filtered.qs.values_list("pk", flat=True))

        self._reset_request(info)
        setattr(info.context, "_visibility_instances_cache", instance_ids)
        return instance_ids
