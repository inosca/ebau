import importlib

import pytest

from camac.instance.models import FormField


@pytest.mark.django_db
def test_fix_sz_false_coordinate_values(
    instance_factory, form_field_factory, set_application_sz
):
    field_name = "punkte"
    fix_me = instance_factory()
    bad_field_value = [
        {"lat": 47.175669937318816, "lng": 8.8984885140077},
        {"lat": 47.175669937318810, "lng": 8.8984885140066},
    ]
    form_field_factory(instance=fix_me, name=field_name, value=bad_field_value)
    good_instance = instance_factory()
    good_instance_field_value = [
        [
            {"lat": 47.175669937318816, "lng": 8.8984885140077},
            {"lat": 47.175669937318810, "lng": 8.8984885140066},
        ],
        [{"lat": 47.175669937318816, "lng": 8.8984885140077}],
    ]
    form_field_factory(
        instance=good_instance, name=field_name, value=good_instance_field_value
    )
    migration = importlib.import_module(
        "camac.instance.migrations.0042_data_fix_sz_punkte_values"
    )
    migration.fix_field_values(FormField)
    assert fix_me.fields.get(name=field_name).value == [
        [obj] for obj in bad_field_value
    ]
    assert good_instance.fields.get(name=field_name).value == good_instance_field_value
