from caluma.caluma_user.views import AuthenticationGraphQLView

from camac.user.models import User


class CamacAuthenticatedGraphQLView(AuthenticationGraphQLView):
    def get_user(self, request, *args, **kwargs):
        oidc_user = super().get_user(request, *args, **kwargs)

        request.camac_user = None
        if oidc_user is not None:
            request.camac_user = User.objects.filter(
                username=oidc_user.username
            ).first()

        return oidc_user
