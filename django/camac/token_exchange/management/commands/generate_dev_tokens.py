from django.conf import settings
from django.core.management.base import BaseCommand

from camac.token_exchange.conftest import encode_token


class Command(BaseCommand):
    help = "Generate tokens to test the token exchange feature in development"

    def handle(self, *args, **options):
        shared_data = {
            "nbf": 1706015466,
            "exp": 32535122400,
            "iat": 1706015466,
            "iss": settings.TOKEN_EXCHANGE_JWT_ISSUER,
        }

        user_token_data = {
            **shared_data,
            "firstName": "John",
            "name": "Doe",
            "profileId": "1",
            "email": "john.doe@example.com",
            "organisationName": "",
        }

        company_token_data = {
            **shared_data,
            "firstName": "Jane",
            "name": "Doe",
            "profileId": "2",
            "email": "jane.doe@acme.com",
            "organisationName": "ACME Inc.",
        }

        user_token = encode_token(
            user_token_data,
            settings.TOKEN_EXCHANGE_JWT_SECRET,
            settings.TOKEN_EXCHANGE_JWE_SECRET,
        )
        company_token = encode_token(
            company_token_data,
            settings.TOKEN_EXCHANGE_JWT_SECRET,
            settings.TOKEN_EXCHANGE_JWE_SECRET,
        )

        self.stdout.write(self.style.SUCCESS("User token: ") + user_token)
        self.stdout.write(self.style.SUCCESS("Company token: ") + company_token)
