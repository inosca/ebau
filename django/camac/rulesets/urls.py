from rest_framework.routers import SimpleRouter

from camac.rulesets.views import ApplicationTypeViewSet, ResponsibleUserRuleViewSet

r = SimpleRouter(trailing_slash=False)

r.register(r"application-types", ApplicationTypeViewSet, "application-type")
r.register(
    r"responsible-user-rules",
    ResponsibleUserRuleViewSet,
    "responsible-user-rule",
)

urlpatterns = r.urls
