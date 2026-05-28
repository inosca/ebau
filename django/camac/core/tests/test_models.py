import pytest
from django.utils.translation import override

from camac.core.models import FormGroup, InstanceResource, Resource


def test_instance_resource_defaults(db, instance_resource):
    new_ir = InstanceResource.objects.create(
        resource_id=instance_resource.resource_id,
        available_instance_resource_id=instance_resource.available_instance_resource_id,
        hidden=0,
    )
    assert new_ir.form_group_id == FormGroup.objects.first().pk
    assert new_ir.sort == instance_resource.sort + 1


def test_resource_defaults(db, resource):
    new_resource = Resource.objects.create(
        available_resource_id=resource.available_resource_id,
        hidden=0,
    )
    assert new_resource.sort == resource.sort + 1


@pytest.mark.parametrize(
    "is_multilingual,current_language,translations,expected_name",
    [
        # multilingual
        # translation for current language exists
        # and is returned
        (True, "de", ["de"], "name de"),
        (True, "fr", ["fr"], "name fr"),
        (True, "de", ["de", "fr"], "name de"),
        (True, "fr", ["de", "fr"], "name fr"),
        # translation for current language does not exist
        # fallback to first available language (defined
        # by order of available languages)
        (True, "de", ["fr"], "name fr"),
        (True, "fr", ["de"], "name de"),
        (True, "de", ["fr", "it"], "name fr"),
        (True, "fr", ["de", "it"], "name de"),
        # no translation in configured available languages
        # exists
        (True, "de", ["it"], None),
        (True, "de", [], None),
        (True, "fr", [], None),
        # not multilingual
        (False, "de", [], "name untranslated"),
        (False, "fr", [], "name untranslated"),
    ],
)
# @pytest.mark.parametrize("model", ["de", "fr"])
def test_multilingual_name_translations(
    db,
    application_settings,
    service,
    service_t_factory,
    is_multilingual,
    current_language,
    translations,
    expected_name,
):
    application_settings["IS_MULTILINGUAL"] = is_multilingual
    application_settings["AVAILABLE_LANGUAGES"] = (
        ["de", "fr"] if is_multilingual else ["de"]
    )

    # remove any pre-existing translations for test
    service.trans.all().delete()

    # only add translations if is multilingual
    if is_multilingual:
        service.name = None
        service.save()

        for language in translations:
            translation = service_t_factory(
                service=service, language=language, name=f"name {language}"
            )
            service.trans.add(translation)

    else:
        service.name = "name untranslated"
        service.save()

    with override(current_language):
        assert service.get_name() == expected_name
        assert str(service)
        if expected_name:
            assert str(service) == expected_name
