class AttributeMixin(object):
    """Methods to help working with attributes on views and serializers."""

    def serializer_getattr(self, attr, default=None):
        """Get attribute first on self, when None do lookup on view."""
        try:
            value = getattr(self, attr)
        except AttributeError:
            # fallback to attribute on view
            view = getattr(self, "context", {}).get("view")
            value = getattr(view, attr, default)

        return value
