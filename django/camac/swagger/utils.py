from drf_yasg import openapi

group_param = openapi.Parameter(
    "x-camac-group",
    openapi.IN_HEADER,
    description="Group ID the request should be made for.",
    type=openapi.TYPE_INTEGER,
    required=True,
)


def get_operation_description(
    companies: list = ["GemDat", "CMI", "Nexplore"], is_preview=False
) -> str:
    """Generate a description for the given operation.

    You can override the list of companies, if one endpoint is only used for some
    of them. If you pass is_preview=True, a slightly different text is generated
    that will warn the users that this is not "set in stone" just yet.
    """
    if not len(companies):  # pragma: no cover
        return ""

    companies_list = f" - {'\n - '.join(companies)}"

    if is_preview:
        return (
            "This endpoint is currently in a **preview** stage. It will likely "
            "remain stable, but may be amended in future versions. It is in use "
            "by the following companies: \n"
            f"{companies_list}"
        )
    return (
        "This endpoint will not change without prior notice. "
        "It is used by the implementations of following companies:\n\n"
        f"{companies_list}"
    )
