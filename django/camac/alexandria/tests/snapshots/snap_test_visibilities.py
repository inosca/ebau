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
