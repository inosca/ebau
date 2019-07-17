# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_instance[work_item_resp0-201-new] 1'] = [
    (
        'http://caluma:8000/graphql/',
        (
        ),
        {
            'headers': {
                'Authorization': b''
            },
            'json': {
                'query': '''
                    query ($case_id: ID!) {
                      node(id:$case_id) {
                        ... on Case {
                          id
                          meta
                          workflow {
                            id
                          }
                          document {
                            id
                            answers(questions: ["gemeinde"]) {
                              edges {
                                node {
                                  id
                                  question {
                                    slug
                                  }
                                  ... on StringAnswer {
                                    stringValue: value
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                ''',
                'variables': {
                    'case_id': 'Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU='
                }
            }
        }
    ),
    (
        'http://caluma:8000/graphql/',
        (
        ),
        {
            'headers': {
                'Authorization': b''
            },
            'json': {
                'query': '''
                       mutation save_instance_id ($input: SaveCaseInput!) {
                         saveCase (input: $input) {
                           case {
                             id
                             meta
                           }
                         }
                       }
                ''',
                'variables': {
                    'input': {
                        'id': 'Q2FzZToxODBlMGQxNy0zZmZkLTQ1ZDMtYTU1MC1kMjVjNGVhODIxNDU=',
                        'meta': '{"camac-instance-id": "XXX"}',
                        'workflow': 'V29ya2Zsb3c6YnVpbGRpbmctcGVybWl0'
                    }
                }
            }
        }
    )
]

snapshots['test_create_instance[new] 1'] = [
    (
        'http://caluma:8000/graphql/',
        (
        ),
        {
            'headers': {
                'Authorization': b''
            },
            'json': {
                'query': '''
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
            ''',
                'variables': {
                    'slug': 'test'
                }
            }
        }
    ),
    (
        'http://caluma:8000/graphql/',
        (
        ),
        {
            'headers': {
                'Authorization': b''
            },
            'json': {
                'query': '''
                mutation CreateDocument($input: SaveDocumentInput!) {
                    saveDocument(input: $input) {
                    document {
                        id
                        meta
                    }
                    }
                }
            ''',
                'variables': {
                    'input': {
                        'form': 'test',
                        'meta': '{"camac-instance-id": "XXX"}'
                    }
                }
            }
        }
    )
]
