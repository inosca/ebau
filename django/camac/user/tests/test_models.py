import pytest

from camac.user.models import Service, User


@pytest.mark.django_db
def test_service_defaults(service):
    new_service = Service.objects.create(service_group_id=service.service_group_id)
    assert new_service.sort == service.sort + 1


@pytest.mark.django_db
def test_service_addressed_work_items(service, caluma_work_item_factory):
    addressed_work_item = caluma_work_item_factory(addressed_groups=[str(service.pk)])
    assert addressed_work_item in service.addressed_work_items


SHARED_EMAIL = "test@example.com"
UNKNOWN_EMAIL = "other@example.com"


@pytest.fixture
def users(user_factory):
    return (
        user_factory(email=SHARED_EMAIL, username="internal"),
        user_factory(email=SHARED_EMAIL, username="egov:123"),
    )


@pytest.mark.parametrize(
    "enable_token_exchange,username_prefix,expect_filtered",
    [
        (True, "egov:", True),
        (False, "egov:", False),
        (True, "", False),
    ],
)
@pytest.mark.django_db
def test_user_queryset_portal_and_internal_users(
    users, settings, enable_token_exchange, username_prefix, expect_filtered
):
    settings.ENABLE_TOKEN_EXCHANGE = enable_token_exchange
    settings.TOKEN_EXCHANGE_USERNAME_PREFIX = username_prefix

    internal_user, portal_user = users
    all_users = [internal_user, portal_user]

    def by_pk(queryset):
        return sorted(queryset, key=lambda user: user.pk)

    assert by_pk(User.objects.portal_users()) == (
        [portal_user] if expect_filtered else all_users
    )
    assert by_pk(User.objects.internal_users()) == (
        [internal_user] if expect_filtered else all_users
    )


@pytest.mark.django_db
def test_user_queryset_only_active(user_factory):
    active_user = user_factory(disabled=0)
    user_factory(disabled=1)

    assert list(User.objects.only_active()) == [active_user]


@pytest.mark.django_db
def test_user_queryset_get_by_username_and_email(user_factory):
    user = user_factory(username="internal", email=SHARED_EMAIL)

    assert User.objects.get_by_username(user.username) == user
    assert User.objects.get_by_username("nope") is None

    assert User.objects.get_by_email(SHARED_EMAIL) == user
    assert User.objects.get_by_email(UNKNOWN_EMAIL) is None
