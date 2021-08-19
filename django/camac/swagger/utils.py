from drf_yasg import openapi

group_param = openapi.Parameter(
    "group",
    openapi.IN_QUERY,
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
