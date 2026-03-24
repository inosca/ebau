import pytest
from django.conf import ImproperlyConfigured
from django.db.models import Q

from camac.document.models import Attachment
from camac.permissions.api import PermissionManager
from camac.permissions.conditions import IsAppeal, Never, Static


@pytest.mark.django_db
def test_custom_conditions_with_static_permissions(
    userinfo,
    be_instance,
    attachment_factory,
    be_permissions_settings,
    be_access_levels,
    service_factory,
    attachment_section_factory,
):
    """Verify permissions behaviour for static permissions."""

    # Give the geometers a static permission
    be_permissions_settings["ACCESS_LEVELS"]["geometer"].extend(
        [
            ("documents-read-internal", Static()),
            ("documents-read-all", Static()),
        ]
    )

    section1 = attachment_section_factory()
    section2 = attachment_section_factory()
    section3 = attachment_section_factory()
    att1 = attachment_factory(instance=be_instance, service=userinfo.service)
    att2 = attachment_factory(instance=be_instance, service=userinfo.service)
    att3 = attachment_factory(instance=be_instance, service=service_factory())
    att4 = attachment_factory(instance=be_instance, service=service_factory())
    att1.attachment_sections.add(section1)
    att2.attachment_sections.add(section2)
    att3.attachment_sections.add(section1)
    att4.attachment_sections.add(section3)

    mgr = PermissionManager(userinfo)
    mgr.grant(
        be_instance,
        grant_type="SERVICE",
        access_level="geometer",
        service=userinfo.service,
    )

    # We can now build a filter like this:
    internal_expr = Q(
        #  In sections 1 and 2, the user can
        # only see "internal" documents, meaning same/own service, if he has
        # the "documents-read-internal" static permission on said instance.
        mgr.static_permission_expr(
            "documents-read-internal", instance_prefix="instance"
        ),
        attachment_sections__in=[section1.pk, section2.pk],
        service=mgr.userinfo.service,
    )
    all_expr = Q(
        # In section 3, all documents are readable if user has the
        # `documents-read-all` static permission
        mgr.static_permission_expr("documents-read-all", instance_prefix="instance"),
        attachment_sections__in=[section3.pk],
    )
    atts = Attachment.objects.filter(all_expr | internal_expr)

    assert att1 in atts  # right service, internal section - visible
    assert att2 in atts  # other section, internal section - also visible
    assert att3 not in atts  # wrong service, not internal - not visible
    assert att4 in atts  # all-readable section, despite other service - visible


def test_static_conditions_not_composable():
    with pytest.raises(ImproperlyConfigured) as excinfo:
        IsAppeal() & Static()
    assert excinfo.match("In IsAppeal & Static: right operand is not composable")

    with pytest.raises(ImproperlyConfigured) as excinfo:
        Static() | Never()
    assert excinfo.match("In Static | Never: left operand is not composable")

    with pytest.raises(ImproperlyConfigured) as excinfo:
        ~Static()
    assert excinfo.match("In ~Static: inner operand is not composable")
