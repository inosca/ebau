from rest_framework.authentication import get_authorization_header

from ..caluma import CalumaClient
from .queries import document_query


def get_document(instance_id, request):
    filter = {"filter": [{"key": "camac-instance-id", "value": instance_id}]}
    caluma = CalumaClient(get_authorization_header(request))

    resp = caluma.query_caluma(
        document_query,
        variables=filter,
        add_headers={"X-CAMAC-GROUP": str(request.group.pk)},
    )
    return resp


# def get_application_xml(instance_id, request):
#     data = get_document(instance_id, request)
#     return data
