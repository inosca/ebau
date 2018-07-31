from camac.user import middleware


def test_get_group_default(admin_rf, admin_user, group):
    request = admin_rf.request()
    request.user = admin_user
    request.auth = {"aud": "unknown"}

    request_group = middleware.get_group(request)
    assert request_group == group


def test_get_group_param(admin_rf, admin_user, user_group_factory):
    new_group = user_group_factory(user=admin_user).group
    request = admin_rf.get("/", data={"group": new_group.pk})
    request.user = admin_user

    group = middleware.get_group(request)
    assert group == new_group
