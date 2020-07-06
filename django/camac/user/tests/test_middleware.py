from camac.user import middleware


def test_get_group_default(rf, admin_user, group):
    request = rf.request()
    request.user = admin_user
    request.auth = {"aud": "unknown"}

    request_group = middleware.get_group(request)
    assert request_group == group


def test_get_group_portal(rf, settings, admin_user, group, group_factory):
    portal_group = group_factory(name="Portal")
    settings.APPLICATION["PORTAL_GROUP"] = portal_group.pk
    request = rf.request()
    request.user = admin_user
    request.auth = {"aud": "portal"}

    request_group = middleware.get_group(request)
    assert request_group == portal_group


def test_get_group_portal_list(rf, settings, admin_user, group, group_factory):
    portal_group = group_factory(name="Portal")
    settings.APPLICATION["PORTAL_GROUP"] = portal_group.pk
    request = rf.request()
    request.user = admin_user
    request.auth = {"aud": ["something", "portal", "else"]}

    request_group = middleware.get_group(request)
    assert request_group == portal_group


def test_get_group_param(rf, admin_user, user_group_factory):
    new_group = user_group_factory(user=admin_user).group
    request = rf.get("/", data={"group": new_group.pk})
    request.user = admin_user

    group = middleware.get_group(request)
    assert group == new_group


def test_get_group_header(rf, admin_user, user_group_factory):
    new_group = user_group_factory(user=admin_user).group
    request = rf.get("/", HTTP_X_CAMAC_GROUP=new_group.pk)
    request.user = admin_user

    group = middleware.get_group(request)
    assert group == new_group
