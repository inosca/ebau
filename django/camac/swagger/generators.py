from drf_yasg.generators import EndpointEnumerator, OpenAPISchemaGenerator


class OptInEnpointEnumerator(EndpointEnumerator):
    def should_include_endpoint(self, path, callback, *args, **kwargs):
        if not super().should_include_endpoint(path, callback, *args, **kwargs):
            return False

        include = getattr(callback.cls, "include_in_swagger", False)

        if callable(include):
            include = include()

        return bool(include)


class OptInOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    endpoint_enumerator_class = OptInEnpointEnumerator
