from drf_yasg import openapi

group_param = openapi.Parameter(
    "group",
    openapi.IN_QUERY,
    description="Group ID the request should be made for.",
    type=openapi.TYPE_INTEGER,
)
