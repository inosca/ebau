import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name,num_queries,size", [
    ('Applicant', 6, 0),
    ('Service', 7, 1),
    ('Municipality', 7, 1),
    ('Canton', 7, 1),
])
def test_notification_template_list(admin_client, notification_template,
                                    num_queries, django_assert_num_queries,
                                    size):
    url = reverse('notificationtemplate-list')
    with django_assert_num_queries(num_queries):
        response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    if size > 0:
        json = response.json()
        assert len(json['data']) == size
        assert json['data'][0]['id'] == str(notification_template.pk)


@pytest.mark.parametrize("role__name", [
    'Canton',
])
def test_circulation_detail(admin_client, notification_template):
    url = reverse(
        'notificationtemplate-detail', args=[notification_template.pk]
    )

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
