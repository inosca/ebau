from datetime import datetime

from django.conf import settings
from django.core.signing import Signer
from django.utils.timezone import make_aware


def validate_captcha_token(request):
    if not settings.APPLICATION.get("ENABLE_PUBLIC_CALUMA_CAPTCHA"):
        return True

    token_str = (request.headers.get("X_CAMAC_PUBLIC_TOKEN") or "").strip()

    # skip captcha auth for authenticated users.
    if not token_str and request.headers.get("Authorization"):
        return True

    signer = Signer()

    try:
        token = signer.unsign_object(token_str)
    except Exception:
        return False

    return token["expiry"] > make_aware(datetime.now()).timestamp()
