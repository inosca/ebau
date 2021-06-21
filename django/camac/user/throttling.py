from rest_framework.throttling import ScopedRateThrottle


class GroupScopedRateThrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):  # pragma: no cover
        return self.cache_format % {
            "scope": self.scope,
            "ident": request.group.pk if request.group else self.get_indent(request),
        }
