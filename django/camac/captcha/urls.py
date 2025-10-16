from captcha import views as captcha_views
from django.conf import settings
from django.urls import re_path

from . import views as views

urlpatterns = []
if settings.APPLICATION.get("ENABLE_PUBLIC_CALUMA_CAPTCHA"):
    urlpatterns += [
        re_path(
            r"captcha/image/(?P<key>\w+)/$",
            captcha_views.captcha_image,
            name="captcha-image",
        ),
        re_path(
            r"captcha/generate/$",
            captcha_views.captcha_refresh,
            name="captcha-generate",
        ),
        re_path(
            r"captcha/validate/(?P<key>\w+)/$",
            views.captcha_validation_view,
            name="captcha-validate",
        ),
    ]
