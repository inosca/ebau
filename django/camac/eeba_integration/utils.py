import logging
from urllib.parse import urlparse

from caluma.caluma_core.exceptions import ConfigurationError
from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, Question
from caluma.caluma_form.validators import CustomValidationError
from django.conf import settings

logger = logging.getLogger(__name__)


def get_answer(question, document):
    """
    Retrieve the value of the Answer model instance.

    Return the answer value if found, otherwise None.
    """
    answer = Answer.objects.filter(question=question, document=document).first()
    return answer.value if answer else None


def save_answer(document, question_slug, answer_value):
    """
    Save an answer for a question.

    This function performs side effects such as retrieving the question and saving the answer.
    It assumes that permission has already been verified.

    Return the updated Answer instance on success, or None if any step fails.
    """
    try:
        question = Question.objects.get(pk=question_slug)
    except Question.DoesNotExist:  # pragma: no cover
        logger.error("Question with slug '%s' does not exist", question_slug)
        return None

    try:
        updated_answer = form_api.save_answer(
            question=question, document=document, value=answer_value
        )
        return updated_answer
    except (ConfigurationError, CustomValidationError) as e:  # pragma: no cover
        logger.error(
            "Failed to save answer for question '%s': %s", question_slug, str(e)
        )
        return None


def extract_integration_id(response):
    """
    Extract the integration ID from the given response.

    First attempt to extract the integration ID from the 'Location' header.
    If not found, fall back to parsing the JSON body.

    Return the extracted integration ID if found, otherwise None.
    """
    location_url = response.headers.get("Location", "").strip()
    integration_id = None
    if location_url:
        parsed_path = urlparse(location_url).path.rstrip("/")
        path_segments = [segment for segment in parsed_path.split("/") if segment]
        if path_segments:
            integration_id = path_segments[-1]

    if not integration_id:
        try:
            integration_id = response.json().get("id")
        except (ValueError, AttributeError):  # pragma: no cover
            integration_id = None

    return integration_id


def exchange_token(session, subject_token):
    data = [
        ("grant_type", "urn:ietf:params:oauth:grant-type:token-exchange"),
        ("client_id", settings.KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT),
        ("client_secret", settings.KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT_SECRET),
        ("subject_token", subject_token),
        ("subject_token_type", "urn:ietf:params:oauth:token-type:access_token"),
        ("requested_token_type", "urn:ietf:params:oauth:token-type:access_token"),
        ("scope", f"openid {settings.KEYCLOAK_EEBA_TOKEN_EXCHANGE_SCOPE}"),
    ]
    resp = session.post(settings.KEYCLOAK_OIDC_TOKEN_URL, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]
