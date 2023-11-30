import pytest
from django.urls import get_resolver
from rest_framework import status

from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.tests.test_instance_public import (  # noqa: F401
    create_caluma_publication,
)


@pytest.fixture
def public_urls(application_settings):
    mixin_urls = []

    for view, urls in get_resolver().reverse_dict.items():
        if not hasattr(view, "cls"):
            continue

        if issubclass(view.cls, InstanceQuerysetMixin):
            mixin_urls.append((view.cls.queryset.model, urls[0][0]))

    return mixin_urls


@pytest.fixture()
def public_data(
    create_caluma_publication,  # noqa: F811
    be_instance,
    attachment_factory,
    issue_factory,
    history_entry_factory,
    journal_entry_factory,
    instance_responsibility_factory,
    form_field_factory,
    workflow_entry_factory,
    communications_topic_factory,
    communications_message_factory,
    objection_factory,
    activation_factory,
    circulation_factory,
    communications_attachment_factory,
    attachment_version_factory,
    billing_v2_entry_factory,
    instance_acl_factory,
):
    attachment = attachment_factory(instance=be_instance, context={"isPublished": True})
    attachment_version_factory(attachment=attachment)
    issue_factory(instance=be_instance)
    history_entry_factory(instance=be_instance)
    journal_entry_factory(instance=be_instance)
    instance_acl_factory(instance=be_instance)
    instance_responsibility_factory(instance=be_instance)
    form_field_factory(instance=be_instance, name="kategorie-des-vorhabens")
    workflow_entry_factory(instance=be_instance)
    topic = communications_topic_factory(instance=be_instance)
    message = communications_message_factory(topic=topic)
    communications_attachment_factory(message=message)
    objection_factory(instance=be_instance)
    circulation = circulation_factory(instance=be_instance)
    activation_factory(circulation=circulation)
    billing_v2_entry_factory(instance=be_instance)

    create_caluma_publication(be_instance)


def test_public_urls(db, public_urls, public_data, admin_client):
    """Test public URLs to see that no data is leaked unintentionally.

    All URLs of views using the InstanceQuerysetMixin are collected and fetched
    to ensure they don't leak information even though the user may see the
    instance itelf (due to it being public).
    """
    allowed_urls = [
        # Public caluma instances
        "/api/v1/public-caluma-instances",
        # Attachments
        "/api/v1/attachments",
        "/api/v1/attachments/%(pk)s",
        "/api/v1/attachments/%(pk)s/thumbnail",
        "/api/v1/attachments/files/",
        # Download paths for attachments and attachment versions. The attachment
        # version must return 403 however.
        "/api/v1/%(path)s",
        # SZ form fields
        "/api/v1/form-fields",
        "/api/v1/form-fields/%(pk)s",
        # alexandria
        "/api/v1/documents",
        "/api/v1/files",
    ]

    for model, url_config in public_urls:
        # Background information: If you run into the below assertion, we
        # need a DB entry for the model mentioned, to ensure this doesn't
        # leak unintentionally. Pull in the corresponding factory in the
        # `public_data` fixture above and instantiate it with a link to
        # `be_instance` so this test can do it's magic.
        assert (
            model.objects.exists()
        ), f"No object found for model {model.__name__} - please create one"

        url_tpl, args = url_config
        url_tpl = f"/{url_tpl}"

        if len(args):
            obj = model.objects.only(*args).first()
            url = url_tpl % {arg: getattr(obj, arg) for arg in args}
        else:
            url = url_tpl

        if url == "/api/v1/attachments/files/":
            url += f"?attachments={model.objects.first().pk}"

        response = admin_client.get(url, HTTP_X_CAMAC_PUBLIC_ACCESS=True)

        if url_tpl not in allowed_urls or (
            url_tpl == "/api/v1/%(path)s" and "attachment-version" in url
        ):
            assert response.status_code in [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            ], f"{url_tpl} is accessible for public users"
        else:
            assert (
                response.status_code == status.HTTP_200_OK
            ), f"{url_tpl} is not accessible for public users"
