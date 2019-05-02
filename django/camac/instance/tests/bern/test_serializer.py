import json

from django.urls import reverse
from rest_framework import status

from camac.instance.models import Instance


def test_create_instance(db, admin_client, mocker, instance_state, form, snapshot):
    recorded_requests = []

    def last_inst_id():
        return Instance.objects.order_by("-instance_id").first().instance_id

    mock_responses = [
        # first response: NG asks caluma for data about our case
        mocker.MagicMock(
            json=lambda: {
                "data": {
                    "node": {
                        "id": "Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU=",
                        "meta": {},
                        "workflow": {"id": "V29ya2Zsb3c6YnVpbGRpbmctcGVybWl0"},
                        "workItems": {
                            "edges": [
                                {
                                    "node": {
                                        "status": "COMPLETED",
                                        "task": {"slug": "fill-form"},
                                    }
                                }
                            ]
                        },
                    }
                }
            },
            status_code=status.HTTP_200_OK,
        ),
        # second response: NG updates case with instance id
        mocker.MagicMock(
            json=lambda: {
                "data": {
                    "saveCase": {
                        "case": {
                            "id": "Q2FzZTphNWVlMDFjNS1kZDc0LTQ2MzQtODgzNC01NDMyNzU2MDZmYTk=",
                            "meta": {"camac-instance-id": last_inst_id()},
                        }
                    }
                }
            },
            status_code=status.HTTP_200_OK,
        ),
    ]

    def mock_post(url, *args, **kwargs):
        recorded_requests.append((url, args, kwargs))
        resp = mock_responses.pop(0)

        return resp

    mocker.patch("requests.post", mock_post)

    case_id = "Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU="
    create_resp = admin_client.post(
        reverse("bern-instance-list"),
        {
            "data": {
                "type": "instances",
                "attributes": {"caluma-case-id": case_id},
                "relationships": {
                    "form": {"data": {"id": form.form_id, "type": "forms"}},
                    "instance-state": {
                        "data": {
                            "id": instance_state.instance_state_id,
                            "type": "instance-states",
                        }
                    },
                },
            }
        },
    )
    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.content

    # make sure meta is updated correctly
    assert json.loads(
        recorded_requests[1][2]["json"]["variables"]["input"]["meta"]
    ) == {"camac-instance-id": last_inst_id()}

    # to validate the rest, we need to "fix" the instance id to use snapshot
    recorded_requests[1][2]["json"]["variables"]["input"]["meta"] = json.dumps(
        {"camac-instance-id": "XXX"}
    )
    snapshot.assert_match(recorded_requests)
