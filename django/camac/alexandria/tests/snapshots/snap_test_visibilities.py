# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_category_visibility[applicant-1-False] 1'] = [
    {
        'id': 'run-too-successful',
        'metainfo': {
            'access': {
                'applicant': 'Admin',
                'municipality': 'Read',
                'service': 'Read'
            }
        }
    }
]

snapshots['test_category_visibility[applicant-1-True] 1'] = [
    {
        'id': 'run-too-successful',
        'metainfo': {
            'access': {
                'applicant': 'Admin',
                'municipality': 'Read',
                'service': 'Read'
            }
        }
    },
    {
        'id': 'various-realize',
        'metainfo': {
        }
    }
]

snapshots['test_category_visibility[municipality-3-False] 1'] = [
    {
        'id': 'run-too-successful',
        'metainfo': {
            'access': {
                'applicant': 'Admin',
                'municipality': 'Read',
                'service': 'Read'
            }
        }
    },
    {
        'id': 'story-thing-piece',
        'metainfo': {
            'access': {
                'municipality': 'Read'
            }
        }
    },
    {
        'id': 'final-state-forget',
        'metainfo': {
            'access': {
                'municipality': 'Read',
                'service': 'Internal'
            }
        }
    }
]

snapshots['test_category_visibility[municipality-3-True] 1'] = [
    {
        'id': 'run-too-successful',
        'metainfo': {
            'access': {
                'applicant': 'Admin',
                'municipality': 'Read',
                'service': 'Read'
            }
        }
    },
    {
        'id': 'story-thing-piece',
        'metainfo': {
            'access': {
                'municipality': 'Read'
            }
        }
    },
    {
        'id': 'final-state-forget',
        'metainfo': {
            'access': {
                'municipality': 'Read',
                'service': 'Internal'
            }
        }
    },
    {
        'id': 'various-realize',
        'metainfo': {
        }
    },
    {
        'id': 'fund-eat-cover',
        'metainfo': {
        }
    },
    {
        'id': 'will-well-see-wish',
        'metainfo': {
        }
    }
]

snapshots['test_category_visibility[service-2-False] 1'] = [
    {
        'id': 'run-too-successful',
        'metainfo': {
            'access': {
                'applicant': 'Admin',
                'municipality': 'Read',
                'service': 'Read'
            }
        }
    },
    {
        'id': 'final-state-forget',
        'metainfo': {
            'access': {
                'municipality': 'Read',
                'service': 'Internal'
            }
        }
    }
]

snapshots['test_category_visibility[service-2-True] 1'] = [
    {
        'id': 'run-too-successful',
        'metainfo': {
            'access': {
                'applicant': 'Admin',
                'municipality': 'Read',
                'service': 'Read'
            }
        }
    },
    {
        'id': 'final-state-forget',
        'metainfo': {
            'access': {
                'municipality': 'Read',
                'service': 'Internal'
            }
        }
    },
    {
        'id': 'various-realize',
        'metainfo': {
        }
    },
    {
        'id': 'will-well-see-wish',
        'metainfo': {
        }
    }
]

snapshots['test_document_visibility[applicant-instance__user0-False] 1'] = [
    {
        'title': 'applicant'
    },
    {
        'title': 'invitee'
    },
    {
        'title': 'municipality'
    }
]

snapshots['test_document_visibility[applicant-instance__user0-True] 1'] = [
    {
        'title': 'applicant'
    },
    {
        'title': 'invitee'
    },
    {
        'title': 'municipality'
    }
]

snapshots['test_document_visibility[municipality-instance__user1-False] 1'] = [
    {
        'title': 'municipality'
    }
]

snapshots['test_document_visibility[municipality-instance__user1-True] 1'] = [
    {
        'title': 'municipality'
    }
]

snapshots['test_document_visibility[public-instance__user3-False] 1'] = [
    {
        'title': 'public'
    }
]

snapshots['test_document_visibility[public-instance__user3-True] 1'] = [
    {
        'title': 'public'
    }
]

snapshots['test_document_visibility[service-instance__user2-False] 1'] = [
    {
        'title': 'service'
    }
]

snapshots['test_document_visibility[service-instance__user2-True] 1'] = [
    {
        'title': 'service'
    }
]
