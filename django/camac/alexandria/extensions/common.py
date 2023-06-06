from django.conf import settings


def get_role(user):
    group = user.group
    perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
    return perms.get(user.camac_role) if group else "public"
