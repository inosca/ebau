from rest_framework.throttling import SimpleRateThrottle


class ECHMessageThrottle(SimpleRateThrottle):
    scope = "ech_message"
    rate = "1/min"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": request.GET.get("last", f"group_{request.group.pk}"),
        }
