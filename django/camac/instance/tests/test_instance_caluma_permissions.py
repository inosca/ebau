import json

import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

FULL_PERMISSIONS = {
    "main": ["read", "write", "write-meta"],
    "sb1": ["read", "write", "write-meta"],
    "sb2": ["read", "write", "write-meta"],
    "nfd": ["read", "write", "write-meta"],
}


@pytest.fixture
def mock_nfd_permissions(requests_mock):
    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps({"data": {"allDocuments": {"edges": []}}}),
    )


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_permissions",
    [
        (
            "Applicant",
            "new",
            {
                "main": [
                    "read",
                    "write",
                    "write-meta",  # write-meta camac-instance-id, submit-date
                ],
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        ("Applicant", "subm", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        (
            "Applicant",
            "correction",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Applicant",
            "rejected",
            {
                "main": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb1",
            {
                "main": ["read"],
                "sb1": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read", "write", "write-meta"],  # write-meta: submit-date
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"], "nfd": []},
        ),
        ("Service", "new", {"main": [], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "subm", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "correction", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "rejected", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "sb1", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "sb2", {"main": ["read"], "sb1": ["read"], "sb2": [], "nfd": []}),
        (
            "Service",
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"], "nfd": []},
        ),
        (
            "Municipality",
            "new",
            {"main": [], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "subm",
            {
                "main": ["read", "write-meta"],  # write-meta: ebau-number
                "sb1": [],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "correction",
            {
                "main": ["read", "write"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "rejected",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "sb1",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "conclusion",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read"],
                "nfd": ["write", "write-meta"],
            },
        ),
        ("Support", "new", FULL_PERMISSIONS),
        ("Support", "subm", FULL_PERMISSIONS),
        ("Support", "correction", FULL_PERMISSIONS),
        ("Support", "rejected", FULL_PERMISSIONS),
        ("Support", "sb1", FULL_PERMISSIONS),
        ("Support", "sb2", FULL_PERMISSIONS),
        ("Support", "conclusion", FULL_PERMISSIONS),
    ],
)
def test_instance_permissions(
    admin_client,
    applicant_factory,
    activation,
    instance,
    expected_permissions,
    use_caluma_form,
    mock_nfd_permissions,
):
    applicant_factory(invitee=instance.user, instance=instance)

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    permissions = response.json()["data"]["meta"]["permissions"]

    assert permissions == expected_permissions


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,caluma_response,expected_nfd_permissions",
    [
        ("Applicant", {"data": {"allDocuments": {"edges": []}}}, []),
        (
            "Applicant",
            {
                "data": {
                    "allDocuments": {"edges": [{"node": {"answers": {"edges": []}}}]}
                }
            },
            [],
        ),
        (
            "Applicant",
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "answers": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "question": {
                                                        "slug": "nfd-tabelle-table"
                                                    },
                                                    "value": [],
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            },
            [],
        ),
        (
            "Applicant",
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "answers": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "question": {
                                                        "slug": "nfd-tabelle-table"
                                                    },
                                                    "value": [
                                                        {
                                                            "answers": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "question": {
                                                                                "slug": "nfd-tabelle-status"
                                                                            },
                                                                            "value": "nfd-tabelle-status-erledigt",
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ],
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            },
            [],
        ),
        (
            "Applicant",
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "answers": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "question": {
                                                        "slug": "nfd-tabelle-table"
                                                    },
                                                    "value": [
                                                        {
                                                            "answers": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "question": {
                                                                                "slug": "nfd-tabelle-status"
                                                                            },
                                                                            "value": "nfd-tabelle-status-erledigt",
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "answers": {
                                                                "edges": [
                                                                    {
                                                                        "node": {
                                                                            "question": {
                                                                                "slug": "nfd-tabelle-status"
                                                                            },
                                                                            "value": "nfd-tabelle-status-in-bearbeitung",
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        },
                                                    ],
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            },
            ["read", "write"],
        ),
        ("Service", {}, []),
        ("Municipality", {}, ["write", "write-meta"]),
        ("Support", {}, ["read", "write", "write-meta"]),
    ],
)
def test_instance_nfd_permissions(
    admin_client,
    applicant_factory,
    activation,
    instance,
    caluma_response,
    expected_nfd_permissions,
    use_caluma_form,
    requests_mock,
):
    requests_mock.post("http://caluma:8000/graphql/", text=json.dumps(caluma_response))

    applicant_factory(invitee=instance.user, instance=instance)

    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert (
        response.json()["data"]["meta"]["permissions"]["nfd"]
        == expected_nfd_permissions
    )
