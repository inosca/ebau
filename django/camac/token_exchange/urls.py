from django.urls import re_path

from camac.token_exchange.views import TokenExchangeView

urlpatterns = [
    re_path(
        r"^auth/token-exchange", TokenExchangeView.as_view(), name="token-exchange"
    ),
]
