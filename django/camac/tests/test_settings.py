from django.conf import settings


def test_applications():
    """Verify that configured applications are valid."""
    valid_perms = settings.APPLICATION['ROLE_PERMISSIONS'].values()

    for app, values in settings.APPLICATIONS.items():
        perms = values.get('ROLE_PERMISSIONS', {})

        invalid_perms = set(perms.values()) - set(valid_perms)
        assert invalid_perms == set(), 'Some permissions are unknown'
