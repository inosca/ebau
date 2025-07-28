from rest_framework_json_api.relations import ResourceRelatedField

from camac.user.models import Service, User


class CalumaUserRelatedField(ResourceRelatedField):
    """Field to fake a relation between a Caluma user field and an eBau user.

    This relation field can be used on serializers using Caluma models (e.g.
    work item) to have a relation to an eBau user without requiring a foreign
    key. Caluma saves the username in a char field that will be used to query
    the respective eBau user.

    In order to use this in a performant way, the field assumes all possibly
    needed users were manually prefetched to a given property on the view.
    """

    queryset = User.objects

    def get_attribute(self, instance):
        """Get related user by username from the prefetched users on the view."""

        username = getattr(instance, self.source)

        if users := getattr(self.context["view"], "_prefetched_users", None):
            return users.get(username, None)

        return User.objects.filter(username=username).first()


class CalumaServiceRelatedField(ResourceRelatedField):
    """Field to fake a relation between a Caluma group field and an eBau service.

    This relation field can be used on serializers using Caluma models (e.g.
    work item) to have a relation to an eBau service. This information is stored
    in an array or char field in Caluma so we can't use regular relation fields.

    In order to use this in a performant way, the field assumes all possibly
    needed services were manually prefetched to a given property on the view.
    """

    queryset = Service.objects

    def get_attribute(self, instance):
        """Get related service from the prefetched services on the view."""

        pk = getattr(instance, self.source)

        if services := getattr(self.context["view"], "_prefetched_services", None):
            return services.get(pk, None)

        return Service.objects.filter(pk=pk).first()
