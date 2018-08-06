def get_request(obj):
    """Get request on given object.

    Tries to locate request as attribute or in context
    attribute.

    Needed for mixins support serializers and views objects.
    """
    request = getattr(obj, "request", None)
    if request is None:
        # on serializer request is in context dict
        request = getattr(obj, "context")["request"]

    return request
