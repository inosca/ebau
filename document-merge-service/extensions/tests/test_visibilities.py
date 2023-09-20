from django.urls import reverse
from rest_framework import status


def test_custom_visibility(admin_client, mock_services, template_factory):
    visible_templates = [
        template_factory(meta={}),
        template_factory(meta={"service": "1"}),
    ]
    invisible_templates = [template_factory(meta={"service": "10"})]

    response = admin_client.get(reverse("template-list"))

    assert response.status_code == status.HTTP_200_OK

    slugs = [item["slug"] for item in response.json()]
    assert len(slugs) == 2

    for template in visible_templates:
        assert template.pk in slugs

    for template in invisible_templates:
        assert template.pk not in slugs
