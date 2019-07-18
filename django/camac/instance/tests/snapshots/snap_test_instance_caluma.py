# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_create_instance[new] 1"] = [
    (
        "http://caluma:8000/graphql/",
        (),
        {
            "headers": {"Authorization": b""},
            "json": {
                "query": """
                query GetMainForm($slug: String!) {
                    allForms(slug: $slug, metaValue: [{key: "is-main-form", value: true}]) {
                        edges {
                            node {
                                slug
                                meta
                            }
                        }
                    }
                }
            """,
                "variables": {"slug": "test"},
            },
        },
    ),
    (
        "http://caluma:8000/graphql/",
        (),
        {
            "headers": {"Authorization": b""},
            "json": {
                "query": """
            mutation CreateDocument($input: SaveDocumentInput!) {
                saveDocument(input: $input) {
                    clientMutationId
                }
            }
            """,
                "variables": {
                    "input": {"form": "test", "meta": '{"camac-instance-id": "XXX"}'}
                },
            },
        },
    ),
]
