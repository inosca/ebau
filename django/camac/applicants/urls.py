from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"applicants", views.ApplicantsView)
r.register(
    r"applicant-confirmations",
    views.ApplicantConfirmationViewSet,
    basename="applicant-confirmations",
)
r.register(
    r"applicant-confirmation-rounds",
    views.ApplicantConfirmationRoundViewSet,
    basename="applicant-confirmation-rounds",
)

urlpatterns = r.urls
