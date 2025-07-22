from django.urls import re_path
from rest_framework.routers import SimpleRouter

from camac.billing import views
from camac.billing.export.views import BillingV2EntryExportView

urlpatterns = [
    re_path(
        r"billing-v2-entries/export$",
        BillingV2EntryExportView.as_view(),
        name="billing-export",
    ),
    re_path(
        r"product-numbers", views.ProductNumbersView.as_view(), name="product-numbers"
    ),
    re_path(
        r"export-invoices", views.ExportInvoicesView.as_view(), name="export-invoices"
    ),
]

r = SimpleRouter(trailing_slash=False)

r.register(r"billing-v2-entries", views.BillingV2EntryViewset, "billing-v2-entry")
r.register(
    r"billing-v2-entry-templates",
    views.BillingV2EntryTemplateViewset,
    "billing-v2-entry-template",
)

urlpatterns.extend(r.urls)
