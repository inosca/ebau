from django.conf import settings


def get_role(user):
    group = user.get_default_group()
    perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
    return perms.get(group.role.name) if group else "public"
