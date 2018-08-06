import pytest
from django.contrib.auth import get_user_model
from rest_framework import exceptions

from camac import relations


def test_form_data_related_field_valid_pk(admin_user):
    field = relations.FormDataResourceRelatedField(
        queryset=get_user_model().objects.all()
    )
    user = field.to_internal_value(admin_user.pk)
    assert user == admin_user


def test_form_data_related_field_inexistent_pk(db):
    field = relations.FormDataResourceRelatedField(
        queryset=get_user_model().objects.all()
    )
    with pytest.raises(exceptions.ValidationError):
        field.to_internal_value(10)


def test_form_data_related_field_invalid_pk(db):
    field = relations.FormDataResourceRelatedField(
        queryset=get_user_model().objects.all()
    )
    with pytest.raises(exceptions.ValidationError):
        field.to_internal_value({"invalid"})
