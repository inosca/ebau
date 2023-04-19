from alexandria.settings import *

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "alexandria.extensions.authentication.CamacAlexandriaAuthentication"
]
OIDC_DRF_AUTH_BACKEND = (
    "alexandria.oidc_auth.authentication.AlexandriaAuthenticationBackend"
)
