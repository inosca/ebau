from django.contrib.admin.apps import AdminConfig


class DjangoAdminConfig(AdminConfig):
    """Overrides the default django.contrib.admin.site.

    This makes it possible to customize the login page.
    """

    default_site = "camac.admin.DjangoAdminSite"
