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
