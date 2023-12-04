from abc import ABCMeta
from functools import wraps
from typing import Callable, Type

from django.conf import settings
from django.utils.module_loading import import_string

from camac.instance.models import Instance

from .api import PermissionManager
from .exceptions import MissingEventHandler


def decision_dispatch_method(fn: Callable) -> Callable:
    """Decorate a function to make it a decision-dispatch method.

    A decision-dispatch method is a way to redirect a function call to
    separate implementations, depending on a decision outcome.

    The "main method" is first called, and it's return value is used as
    the decision. Then, we look for an implementation that's registered for
    the given decision result. It is then called with the same parameters.

    Example:
    >>> class Foo:
    ...     @decision_dispatch_method
    ...     def do_thing(self):
    ...         # just toss a coin
    ...         return random.choice(['heads', 'tails'])
    ...
    ...     @do_thing.register('heads')
    ...     def do_thing_for_heads(self):
    ...         return "yep, coin landed heads-up"
    ...
    ...     @do_thing.register('tails')
    ...     def do_thing_for_tails(self):
    ...         return "yep, coin landed tails-up"
    ...
    ...     @do_thing.register('edge')
    ...     def do_thing_for_edge(self):
    ...         return "this never happens, for real!"
    """
    _registry = {}

    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        decision_result = fn(self, *args, **kwargs)
        if decision_result not in _registry:
            owner = type(self).__name__
            name = fn.__name__

            raise MissingEventHandler(
                f"{owner}.{name}: No implementation "
                f"registered for {decision_result!r}"
            )
        impl = _registry[decision_result]
        return impl(self, *args, **kwargs)

    def register(decision):
        """Register this method for the given decision outcome."""

        def decorator(fn):
            _registry[decision] = fn
            return fn

        return decorator

    # setattr() is accepted by ruff, "wrapped.register =.." is no bueno
    setattr(wrapped, "register", register)
    return wrapped


class EventTrigger:
    def __set_name__(self, owner, name):
        self.name = name

    def __call__(self, request, *args, **kwargs):
        handler = get_event_handler_class().from_request(request)
        handler.default_event = self.name
        # execute the event handler function, which in turn
        # will grant/revoke ACLs as needed
        return getattr(handler, self.name)(*args, **kwargs)


class Trigger:
    """Contains any event that may cause a permissions change."""

    decision_decreed = EventTrigger()


class PermissionEventHandler(metaclass=ABCMeta):
    """Base class for handling permissions-related events.

    This class implements some infrastructure and defines all the events
    that may have an impact on the permissions module.

    The idea is that there is a subclass for each Canton, which will
    implement the event handlers and grant/revoke the permissions as required
    in that canton.

    Some utilities and helpers are provided to make the work as simple as
    possible
    """

    def __init__(self, manager: PermissionManager):
        self.manager = manager

    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)

        """Validate the completeness of the event handler subclass."""
        for name, value in vars(Trigger).items():
            if isinstance(value, EventTrigger):  # pragma: no cover
                # This is for code validation and should never happen IRL,
                # so no coverage required
                assert hasattr(cls, name), f"{cls} is missing implementation for {name}"

    @classmethod
    def from_request(cls, request):
        """Initialize the event handler from a (REST) request."""
        return cls(manager=PermissionManager.from_request(request))


class EmptyEventHandler(PermissionEventHandler):
    """An empty permissions event handler.

    This just does nothing. It is used as a fallback, when no event
    handler is registered for a given client / application.

    It implements every relevant event handler, but with no actual
    effects.
    """

    def decision_decreed(self, instance: Instance):
        return  # pragma: no cover


def get_event_handler_class() -> Type[PermissionEventHandler]:
    """Return the configured event handler class.

    The event handler class is the place where all the permissions-specific
    event handlers should be implemented.
    It should grant and revoke permissions at the appropriate times.
    """

    handler_name = settings.PERMISSIONS.get("EVENT_HANDLER")

    # Fallback to the empty event handler if none has been configured
    return import_string(handler_name) if handler_name else EmptyEventHandler
