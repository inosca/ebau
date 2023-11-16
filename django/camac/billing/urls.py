from rest_framework.routers import SimpleRouter

from camac.billing import views

r = SimpleRouter(trailing_slash=False)

r.register(r"billing-v2-entries", views.BillingV2EntryViewset, "billing-v2-entry")

urlpatterns = r.urls
