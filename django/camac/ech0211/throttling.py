import time

from rest_framework.throttling import SimpleRateThrottle


class ECHMessageThrottle(SimpleRateThrottle):
    scope = "ech_message"
    rate = "1/min"

    # mitigate https://github.com/spulec/freezegun/issues/382
    # see https://github.com/encode/django-rest-framework/pull/7955#issuecomment-830312565
    timer = staticmethod(time.time)

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": request.GET.get("last", f"group_{request.group.pk}"),
        }
