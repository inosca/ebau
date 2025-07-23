import logging
from functools import wraps

import requests
from django.http import response as http_response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class EebaHandlerBadRequestException(Exception):
    """Exception for errors that should result in a 400 Bad Request response."""

    pass


class EebaHandlerServerException(Exception):
    """Exception for errors that should result in a 500 Internal Server Error response."""

    pass


def handle_eeba_client_exceptions(function):
    """
    Handle exceptions for client methods decorator.

    Catch specific exceptions and log them, then re‑raise
    either a BadRequest or ServerException depending on the error.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        operation_name = function.__name__
        try:
            return function(*args, **kwargs)
        except (EebaHandlerServerException, EebaHandlerBadRequestException):
            raise  # pragma: no cover
        except ValueError as e:
            logger.exception(("Bad request error in %s: %s"), operation_name, e)
            raise EebaHandlerBadRequestException(
                ("Bad request in %s: %s") % (operation_name, e)
            ) from e
        except (requests.exceptions.RequestException, TimeoutError) as e:
            logger.exception(("Server error in %s: %s"), operation_name, e)
            raise EebaHandlerServerException(
                ("Server error in %s: %s") % (operation_name, e)
            ) from e
        except Exception as e:  # pragma: no cover
            logger.exception(("Unexpected error in %s: %s"), operation_name, e)
            raise EebaHandlerServerException(
                ("An unexpected error occurred in %s.") % operation_name
            ) from e

    return wrapper


def handle_view_exceptions(view_method):
    """
    Handle exceptions for Eeba Integration Views methods decorator.

    Catch specific exceptions, log them and return the appropriate Response.
    """

    @wraps(view_method)
    def wrapper(self, request, *args, **kwargs):
        view_name = view_method.__name__
        try:
            return view_method(self, request, *args, **kwargs)
        except PermissionDenied as e:
            logger.error("Permission denied error in %s: %s", view_name, e)
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except http_response.Http404 as e:
            logger.error("Not found error %s: %s", view_name, e)
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:  # pragma: no cover
            logger.exception("Unexpected error in %s: %s", view_name, e)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
