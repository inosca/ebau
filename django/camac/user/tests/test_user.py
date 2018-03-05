def test_check_password(admin_user):
    assert admin_user.check_password('password')
    assert not admin_user.check_password('invalid')
