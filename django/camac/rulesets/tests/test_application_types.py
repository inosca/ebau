from django.urls import reverse
from rest_framework import status


def test_application_type_list(db, admin_client, caluma_form_factory, snapshot):
    caluma_form_factory(is_published=False, meta={"is-main-form": True})
    caluma_form_factory(is_published=True)

    main_form = caluma_form_factory(is_published=True, meta={"is-main-form": True})

    response = admin_client.get(reverse("application-type-list"))

    assert response.status_code == status.HTTP_200_OK

    result = response.json()
    assert result == snapshot
    assert len(result["data"]) == 1
    assert result["data"][0]["id"] == main_form.pk
