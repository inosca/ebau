import json
from datetime import datetime, timedelta

from captcha.validators import captcha_validate
from django.core.signing import Signer
from django.http import HttpResponse
from django.utils.timezone import make_aware
from rest_framework import exceptions, status


def captcha_validation_view(request, key):
    json_data = json.loads(request.body.decode("utf-8"))
    challenge = json_data.get("challenge", "")

    try:
        captcha_validate(key, challenge)
    except exceptions.ValidationError:
        return HttpResponse(
            json.dumps({"success": False, "error": "Invalid captcha"}),
            content_type="application/json",
            status=status.HTTP_403_FORBIDDEN,
        )

    signer = Signer()
    expiry = make_aware(datetime.now() + timedelta(minutes=15))
    to_json_response = {
        "success": True,
        "token": signer.sign_object({"key": key, "expiry": expiry.timestamp()}),
    }

    return HttpResponse(
        json.dumps(to_json_response),
        content_type="application/json",
    )
