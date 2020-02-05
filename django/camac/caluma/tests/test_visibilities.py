import pytest

from camac.caluma.extensions.visibilities import CustomVisibility


@pytest.mark.parametrize(
    "role__name,expected_count", [("Support", 3), ("Service", 1), ("Applicant", 0)]
)
def test_visibilities(
    db,
    role,
    expected_count,
    instance_factory,
    group_factory,
    activation_factory,
    admin_info,
):
    group = group_factory(pk=5, role=role)
    admin_info.context.META["HTTP_X_CAMAC_GROUP"] = "5"
    instance = instance_factory(group=group)
    activation_factory(circulation__instance=instance, service=group.service)
    instance_factory(group=group)
    instance_factory()

    v = CustomVisibility()
    qs = v._all_visible_instances(admin_info)
    assert len(qs) == expected_count
