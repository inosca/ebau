"""Helpers for filtering caluma workflow events by task or workflow.

The events extensions (`camac/caluma/extensions/events/*.py`) register handlers
for caluma workflow signals. Most handlers are only relevant for a specific task
or workflow. A handler can declare its relevance declaratively by matching
against either:

- a static slug (e.g. `"formal-exam"`), or
- a slug configured per canton in a settings module such as
  `settings.DISTRIBUTION` or `settings.ADDITIONAL_DEMAND`, addressed through
  `setting(module_name, key)`.

Both kinds can be combined in a single filter:

    @on(post_complete_work_item, raise_exception=True)
    @filter_by_task("formal-exam", setting("DECISION", "TASK"))
    def handle(sender, work_item, user, context=None, **kwargs):
        ...
"""

from itertools import chain
from typing import Any, Callable

from caluma.caluma_core.events import filter_events
from django.conf import settings

from camac.settings.utils import is_module_enabled
from camac.utils import get_dict_item

Source = str | Callable[[], list]
"""A task or workflow source.

Either a static slug (`str`) or a zero-argument callable returning a list of
slugs (as produced by `setting`).
"""


def get_settings(module_name: str, keys: str | list[str]) -> list[Any]:
    """Resolve the configured value(s) for the given settings key(s).

    Looks each key up within `settings.<module_name>` (e.g.
    `settings.DISTRIBUTION`) and returns the configured values, dropping any
    keys that are unset. Nested values can be addressed with a dotted path,
    e.g. `"WORK_ITEM.TASK"`.

    Args:
        module_name: Name of the settings module, e.g. `"DISTRIBUTION"`.
        keys: A single settings key (or dotted path) or a list of them.

    Returns:
        The configured values (e.g. task or workflow slugs) for the keys.
    """

    if not isinstance(keys, list):
        keys = [keys]

    module_settings = getattr(settings, module_name)

    return [
        value
        for key in keys
        if (value := get_dict_item(module_settings, key, default=None))
    ]


def setting(module_name: str, keys: str | list[str]) -> Callable[[], list[Any]]:
    """Defer a settings lookup for use as a task/workflow source.

    Returns a callable that resolves the given key(s) within
    `settings.<module_name>` when the event fires (see `get_settings`). Pass it
    to `filter_by_task` / `filter_by_workflow` to match configured slugs,
    optionally alongside static literal slugs.

    Args:
        module_name: Name of the settings module, e.g. `"DECISION"`.
        keys: One or more settings keys (dotted paths allowed), e.g. `"TASK"`.

    Returns:
        A zero-argument callable returning the configured slug(s).

    Example:
        >>> filter_by_task("formal-exam", setting("DECISION", "TASK"))
    """
    return lambda: get_settings(module_name, keys)


def application_setting(keys: str | list[str]) -> Callable[[], list[Any]]:
    """Defer a `settings.APPLICATION` lookup for use as a task/workflow source.

    This is intentionally separate from `setting` rather than a mere shorthand:
    `settings.APPLICATION` is the main per-canton application config, not a
    module loaded through `load_module_settings`. It currently happens to
    support the same key lookup, but that overlap is incidental and not
    guaranteed to hold. Keeping a dedicated helper makes it explicit at the
    call site that a value comes from `settings.APPLICATION` and not from a
    settings module.

    Args:
        keys: A single settings key (or dotted path) or a list of them,
              e.g. `"CALUMA.AUDIT_TASK"`.

    Returns:
        A zero-argument callable returning the configured slug(s).

    Example:
        >>> filter_by_task(application_setting("CALUMA.AUDIT_TASK"))
    """
    return setting("APPLICATION", keys)


def _resolve(sources: tuple[Source, ...]) -> list[str]:
    """Flatten task/workflow sources into a list of slugs.

    Static slugs are taken verbatim; callables (from `setting`) are invoked and
    their results spread in.
    """
    return list(
        chain(
            *[[source] if isinstance(source, str) else source() for source in sources]
        )
    )


def filter_by_workflow(*workflows: Source) -> Callable:
    """Build an event filter matching a case against the given workflow(s).

    The decorated handler only runs when the event's case belongs to one of the
    given workflows.

    **If possible, static slugs should be avoided in favor of using slugs from
    module settings or adding it to a module setting.**

    Args:
        workflows: One or more workflow sources, each a static slug or a
                  `setting(...)` reference.

    Returns:
        An event filter decorator for the matching workflow(s).

    Example:
        >>> @on(post_complete_case, raise_exception=True)
        ... @filter_by_workflow(setting("ADDITIONAL_DEMAND", "WORKFLOW"))
        ... def handle_completed(sender, case, user, context=None, **kwargs):
        ...     ...
    """

    def filter_fn(case):
        return case.workflow_id in _resolve(workflows)

    return filter_events(filter_fn)


def filter_by_task(*tasks: Source) -> Callable:
    """Build an event filter matching a work item against the given task(s).

    The decorated handler only runs when the event's work item belongs to one of
    the given tasks.

    **If possible, static slugs should be avoided in favor of using slugs from
    module settings or adding it to a module setting.**

    Args:
        tasks: One or more task sources, each a static slug or a `setting(...)`
               reference.

    Returns:
        An event filter decorator for the matching task(s).

    Example:
        >>> @on(post_create_work_item, raise_exception=True)
        ... @filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
        ... def handle_inquiry(sender, work_item, user, context=None, **kwargs):
        ...     ...
    """

    def filter_fn(work_item):
        return work_item.task_id in _resolve(tasks)

    return filter_events(filter_fn)


def filter_by_canton(*cantons: str) -> Callable:
    """Build an event filter matching the configured canton.

    Useful in combination with `filter_by_task` / `filter_by_workflow` for
    handlers that are specific to one or more cantons.

    Args:
        cantons: One or more canton names to match against
                 `settings.APPLICATION_NAME`, e.g. `"kt_gr"`.

    Returns:
        An event filter decorator that only passes for the given canton(s).

    Example:
        >>> @on(post_complete_work_item, raise_exception=True)
        ... @filter_by_canton("kt_so")
        ... def handle(sender, work_item, user, context=None, **kwargs):
        ...     ...
    """
    return filter_events(lambda: settings.APPLICATION_NAME in cantons)


def if_module_enabled(module_name: str) -> Callable:
    """Build an event filter passing only when a module is enabled.

    Delegates to `is_module_enabled`, which handles both config shapes produced
    by `load_module_settings` (pydantic with an `enabled` flag, or dict-based).

    Args:
        module_name: Name of the settings module, e.g. `"DEADLINES"`.

    Returns:
        An event filter decorator that only passes when the module is enabled.

    Example:
        >>> @on(post_create_work_item, raise_exception=True)
        ... @if_module_enabled("DEADLINES")
        ... def handle(sender, work_item, user, context=None, **kwargs):
        ...     ...
    """
    return filter_events(lambda: is_module_enabled(getattr(settings, module_name)))
