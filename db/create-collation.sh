#!/bin/bash
set -e

# This is only used in our testing environment as in other environments a django
# migration creates this collation:
# django/camac/core/migrations/0109_case_insensitive_collation.py
# definition of locale: und-u-ks-level2
#   und: undetermined language, sorts symbols first, then alphabetically per script.
#   -u-: Unicode "Extension U" keyword
#   ks-level2: collation strength level 2, doesn’t include case in comparisons, only letters and accents
psql -d template1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE COLLATION case_insensitive (
        provider = icu,
        locale = 'und-u-ks-level2',
        deterministic = false
    );
EOSQL
