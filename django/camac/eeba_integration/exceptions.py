import logging
from functools import wraps

import requests
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class EebaHandlerBadRequestException(Exception):
    """Exception for errors that should result in a 400 Bad Request response."""

    pass


class EebaHandlerServerException(Exception):
    """Exception for errors that should result in a 500 Internal Server Error response."""

    pass


def handle_exceptions(function):
    """
    Handle exceptions for EebaHandler methods decorator.

    catch specific exceptions and log them, then re‑raise
    either a BadRequest or ServerException depending on the error.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        operation_name = function.__name__
        try:
            return function(*args, **kwargs)
        except (EebaHandlerServerException, EebaHandlerBadRequestException):
            raise
        except ValueError as e:
            logger.exception(_("Bad request error in %s: %s"), operation_name, e)
            raise EebaHandlerBadRequestException(
                _("Bad request in %s: %s") % (operation_name, e)
            ) from e
        except (requests.exceptions.RequestException, TimeoutError) as e:
            logger.exception(_("Server error in %s: %s"), operation_name, e)
            raise EebaHandlerServerException(
                _("Server error in %s: %s") % (operation_name, e)
            ) from e
        except Exception as e:  # pragma: no cover
            logger.exception(_("Unexpected error in %s: %s"), operation_name, e)
            raise EebaHandlerServerException(
                _("An unexpected error occurred in %s.") % operation_name
            ) from e

    return wrapper


def handle_view_exceptions(view_method):
    """
    Handle exceptions for APIView methods decorator.

    catch specific exceptions, log them and return the appropriate Response.
    """

    @wraps(view_method)
    def wrapper(self, request, *args, **kwargs):
        view_name = view_method.__name__
        try:
            return view_method(self, request, *args, **kwargs)
        except EebaHandlerBadRequestException as e:
            logger.error("Bad request error in %s: %s", view_name, e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except EebaHandlerServerException as e:
            logger.error("Server error in %s: %s", view_name, e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:  # pragma: no cover
            logger.exception("Unexpected error in %s: %s", view_name, e)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
