from django.urls import reverse
from rest_framework import status

from . import models


def test_attachment_section_list(admin_user, admin_client,
                                 attachment_section_factory,
                                 attachment_section_role_acl_factory,
                                 attachment_section_group_acl_factory):

    # 1st valid case: attachment section allowed by role acl
    attachment_section_role = attachment_section_factory(sort=1)
    attachment_section_role_acl_factory(
        attachment_section=attachment_section_role,
        role=admin_user.groups.first().role,
        mode=models.ADMIN_PERMISSION,
    )
    # 2nd valid case: attachment section allowed by group acl
    attachment_section_group = attachment_section_factory(sort=2)
    attachment_section_group_acl_factory(
        attachment_section=attachment_section_group,
        group=admin_user.groups.first(),
        mode=models.WRITE_PERMISSION,
    )
    # 1st invalid case: attachment section without acl
    attachment_section_factory()

    url = reverse('attachment-section-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 2
    assert json['data'][0]['id'] == str(attachment_section_role.pk)
    assert json['data'][0]['meta']['mode']  == models.ADMIN_PERMISSION
    assert json['data'][1]['id'] == str(attachment_section_group.pk)
    assert json['data'][1]['meta']['mode']  == models.WRITE_PERMISSION


def test_attachment_section_detail(admin_client, attachment_section):
    url = reverse('attachment-section-detail', args=[attachment_section.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
