import pytest
from django.core.management import call_command

from camac.core.models import (
    AvailableInstanceResource,
    AvailableResource,
    FormGroup,
    InstanceResource,
    InstanceResourceT,
    Resource,
    ResourceT,
)


@pytest.fixture
def translation_ok(db):
    ar_ok = AvailableResource.objects.create(
        available_resource_id="search", module_name="test", controller_name="test"
    )
    resource_ok = Resource.objects.create(
        name="Test", description="A test", hidden=0, sort=0, available_resource=ar_ok
    )
    ResourceT.objects.create(language="de", name="Meine Dossiers", resource=resource_ok)
    air_ok = AvailableInstanceResource.objects.create(
        available_instance_resource_id="Test",
        module_name="test",
        controller_name="test",
    )
    form_group = FormGroup.objects.create(name="Test", description="A test")
    ir_ok = InstanceResource.objects.create(
        name="Test",
        description="A Test",
        hidden=0,
        sort=0,
        available_instance_resource=air_ok,
        form_group=form_group,
        resource=resource_ok,
    )
    InstanceResourceT.objects.create(
        language="de", name="Bauwerk", instance_resource=ir_ok
    )
    return ir_ok


@pytest.fixture
def translation_not_ok(db):
    ar_not_ok = AvailableResource.objects.create(
        available_resource_id="foobar", module_name="test", controller_name="test"
    )
    resource_not_ok = Resource.objects.create(
        name="Test",
        description="A test",
        hidden=0,
        sort=0,
        available_resource=ar_not_ok,
    )
    ResourceT.objects.create(
        language="de", name="Meine Dossiers", resource=resource_not_ok
    )
    air_not_ok = AvailableInstanceResource.objects.create(
        available_instance_resource_id="foobar",
        module_name="test",
        controller_name="test",
    )
    form_group = FormGroup.objects.create(name="Test", description="A test")
    ir_not_ok = InstanceResource.objects.create(
        name="Test",
        description="A Test",
        hidden=0,
        sort=0,
        available_instance_resource=air_not_ok,
        form_group=form_group,
        resource=resource_not_ok,
    )
    InstanceResourceT.objects.create(
        language="en", name="thisdoesntexist", instance_resource=ir_not_ok
    )
    return ir_not_ok


def test_translate(translation_ok, translation_not_ok):
    call_command("translate_camac")
    translations_ok = InstanceResourceT.objects.filter(instance_resource=translation_ok)
    translations_not_ok = InstanceResourceT.objects.filter(
        instance_resource=translation_not_ok
    )

    assert translations_ok.get(language="fr").name == "Ouvrage"
    with pytest.raises(Exception) as e:
        assert translations_not_ok.get(language="fr").name
    assert str(e.value) == "InstanceResourceT matching query does not exist."
    call_command("translate_camac")
    assert translations_ok.get(language="fr").name == "Ouvrage"
