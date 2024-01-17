import io
import itertools
from typing import Any, Optional
from urllib.parse import parse_qsl

import requests
from django.conf import settings
from docxtpl import DocxTemplate
from rest_framework import exceptions

from camac import jinja
from camac.constants import kt_uri as uri_constants


class DocxRenderer:
    """Render docx templates with the specified data.

    :param path: Path to the template
    :type  path: str
    :param data: Data to render the template with
    :type  data: dict
    """

    def __init__(self, path, data):
        self.path = path

        self.buffer = io.BytesIO()
        doc = DocxTemplate(path)
        doc.render(data, jinja.get_jinja_env())
        doc.save(self.buffer)

    @property
    def buffer(self):
        self.__buffer.seek(0)
        return self.__buffer

    @buffer.setter
    def buffer(self, value):
        self.__buffer = value

    def convert(self, to_type="docx"):
        """Convert template to given format using unoconv.

        See: https://github.com/zrrrzzt/tfk-api-unoconv

        :param to_type: File type to convert the template to.
        :type  to_type: str

        :return: Buffer of converted templated.
        :rtype: io.BytesIO
        """

        if to_type == "docx":
            return self.buffer

        url = build_url(settings.UNOCONV_URL, f"/unoconv/{to_type}")

        response = requests.post(url, files={"file": self.buffer})

        if response.status_code != 200:
            raise exceptions.ParseError(
                f"Unoconv failed to convert document {self.path} to type {to_type}"
            )

        result = io.BytesIO(response.content)
        result.seek(0)

        return result


def flatten(data):
    return list(itertools.chain(*data))


def build_url(*fragments, **options):
    separator = options.get("separator", "/")

    url = separator.join([str(fragment).strip(separator) for fragment in fragments])

    if options.get("trailing", False):
        url += separator

    return url


def filters(request):
    """Extract Camac NG filters from request.

    The filters are expected to be a URLencoded string (foo=bar&baz=blah).
    """
    return dict(parse_qsl(request.META.get("HTTP_X_CAMAC_FILTERS", "")))


def order(request):
    """Extract Camac NG order from request.

    The order is expected to be a comma-separated string of fields (foo,bar).
    """
    order = request.META.get("HTTP_X_CAMAC_ORDER", None)
    return order.split(",") if order else None


def headers(info):  # pragma: todo cover
    # TODO: Will be included in coverage again in refactoring of caluma extensions.
    """Extract headers from request."""
    return {
        "x-camac-group": info.context.META.get("HTTP_X_CAMAC_GROUP", None),
        "authorization": info.context.META.get("HTTP_AUTHORIZATION", None),
    }


def get_paper_settings(key=None):
    roles = settings.APPLICATION.get("PAPER", {}).get("ALLOWED_ROLES", {})
    service_groups = settings.APPLICATION.get("PAPER", {}).get(
        "ALLOWED_SERVICE_GROUPS", {}
    )

    if isinstance(key, str):
        key = key.upper()

    return {
        "ALLOWED_ROLES": roles.get(key, roles.get("DEFAULT", [])),
        "ALLOWED_SERVICE_GROUPS": service_groups.get(
            key, service_groups.get("DEFAULT", [])
        ),
    }


def get_responsible_koor_service_id(form_id):
    for service_id, forms in uri_constants.RESPONSIBLE_KOORS.items():
        if form_id in forms:
            return service_id

    raise RuntimeError(
        f"No responsible KOOR found for form id {form_id}"
    )  # pragma: no cover


def is_lead_role(group):
    role_name = group.role.name
    role_mapping = settings.APPLICATION.get("GENERALIZED_ROLE_MAPPING")
    role = role_mapping[role_name] if role_mapping else role_name
    return role.endswith("-lead") or role == "subservice"


def has_permission_for_inquiry_document(group, document):
    from caluma.caluma_workflow.models import WorkItem

    if not document:
        return False  # pragma: no cover

    return (
        document.work_item.status == WorkItem.STATUS_SUSPENDED
        or (document.work_item.status == WorkItem.STATUS_READY and is_lead_role(group))
    ) and str(group.service_id) in document.work_item.controlling_groups


def has_permission_for_inquiry_answer_document(group, document):
    from caluma.caluma_workflow.models import WorkItem

    if not document:
        return False  # pragma: no cover

    return (
        document.case.parent_work_item.status == WorkItem.STATUS_READY
        and str(group.service_id) in document.case.parent_work_item.addressed_groups
    )


def clean_join(*parts: Any, separator: Optional[str] = " ") -> str:
    """Join all truthy arguments as trimmed string with a given separator.

    >>> clean_join(" John", None, "", " Smith ")
    "John Smith"
    """

    return separator.join([str(part).strip() for part in parts if part]).strip()


class _SENTINEL:
    # a standalone sentinel is better than `None`, as `None` could be a
    # useful default passed by the caller. Nobody will accidentally call
    # `get_dict_item()` with a default that is identical to this
    pass


def get_dict_item(obj, item, sep=".", default=_SENTINEL):
    """Return an item from a nested dict structure.

    Example:
    >>> some_dict = {
    >>>     "foo": {
    >>>         "bar": { "baz": 3}
    >>>     }
    >>> }
    >>> get_dict_item(some_dict, 'foo.bar.baz')
    3

    >>> # If your keys contain dots, you can use another separator:
    >>> get_dict_item(some_dict, 'foo!bar!baz', sep="!")
    3

    If a key is not found at any stage, a KeyError is raised. If
    you pass a default value, it is returned instead
    """
    path = item.split(sep)
    prefix = []
    for key in path:
        prefix.append(key)
        try:
            obj = obj[key]
        except (KeyError, TypeError) as exc:
            if default is _SENTINEL:
                err = sep.join(prefix)
                raise KeyError(err) from exc
            return default
    return obj


def get_function_kwargs(callback, possible_kwargs):
    """Return only the kwargs that the given callable accepts.

    This is useful if different callbacks can be configured, and
    you don't want every implementation to take every possible argument.

    Example:
    >>> def foo(x, y):
    >>>     pass
    >>> possible_args = {"x": 1, "y": 2, "z": 3, "a": 99}
    >>> get_function_kwargs(foo, possible_args)
    {"x": 1, "y": 2}

    NOTE: This does not work with functions that accept **kwargs (or *args for
    that matter). It *could* be done, but we had no requirements for it, and it
    would add quite a bit of complexity
    """

    # Figure out which is the *actual* callable - so we can support both
    # plain functions and objects with a __call__() method.
    code = getattr(callback, "__code__", None) or callback.__call__.__code__

    new_kwargs = {}
    for k, v in possible_kwargs.items():
        # we use __call__ so callable objects work as well.
        # A pure function also has __call__, so we can just always use that
        if k in code.co_varnames:
            new_kwargs[k] = v

    return new_kwargs


def call_with_accepted_kwargs(func, **kwargs):
    """Call the given function, but pass on only the kwargs that it accepts.

    You can pass in as many kwargs as are available, but the called function
    does not need to accept them all if it doesn't need them. This simplifies
    generic callback interface design.

    Example:
    >>> def foo(x, y):
    >>>     print(f"x={x}, y={y}")
    >>> call_with_accepted_kwargs(foo, x=3, y=5, z=99, a=1)
    x=3, y=5
    """
    accepted_kwargs = get_function_kwargs(func, kwargs)
    return func(**accepted_kwargs)
