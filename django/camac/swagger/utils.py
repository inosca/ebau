from drf_yasg import openapi

group_param = openapi.Parameter(
    "x-camac-group",
    openapi.IN_HEADER,
    description="Group ID the request should be made for.",
    type=openapi.TYPE_INTEGER,
)


def get_operation_description(companies: list = ["GemDat", "CMI", "Nexplore"]) -> str:
    if not len(companies):  # pragma: no cover
        return ""

    sep = "\n - "
    return (
        "This endpoint will not change without prior notice.\n\n"
        "It is used by the implementations of following companies:\n\n"
        f" - {sep.join(companies)}"
    )


def conditional_factory(when_ok, check_callback):
    """Return a factory to delay a check to call time.

    The returned factory will call the `when_ok` function (may be a class, ...)
    with the given parameters, but only if the `check_callback` returns True.
    Otherwise, `None` is returned.

    Useful for checking settings at run-time instead of startup-time.
    """

    def the_actual_factory(*args, **kwargs):
        if check_callback():
            return when_ok(*args, **kwargs)

    return the_actual_factory
