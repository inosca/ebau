from django.contrib.admin import AdminSite


class DjangoAdminSite(AdminSite):
    login_template = "login.html"
