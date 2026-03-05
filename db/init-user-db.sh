#!/bin/bash
set -e

# Create DB for metabase (only used in SZ)
createdb -U $POSTGRES_USER metabase

# Alter template1 DB which will act as template for the cantonal DBs. This will:
#
# 1. Install necessary extensions
# 2. Create separate schemas for keycloak and DMS to avoid collisions
# 3. Define a case_insensitive collation
#
# The case insensitive collation must be created in the template DB for the
# testing environments to work as they don't run the regular django migrations
# in order to speed up the testing setup. Normally, this django migration would
# create that collation: django/camac/core/migrations/0109_case_insensitive_collation.py
#
# definition of locale: und-u-ks-level2
#   und: undetermined language, sorts symbols first, then alphabetically per script.
#   -u-: Unicode "Extension U" keyword
#   ks-level2: collation strength level 2, doesn’t include case in comparisons, only letters and accents
psql -d template1 -U $POSTGRES_USER <<-EOSQL
    -- Create necessary extensions
    CREATE EXTENSION citext;
    CREATE EXTENSION hstore;
    CREATE EXTENSION "uuid-ossp";

    CREATE SCHEMA keycloak AUTHORIZATION $POSTGRES_USER;
    CREATE SCHEMA dms AUTHORIZATION $POSTGRES_USER;

    CREATE COLLATION case_insensitive (
        provider = icu,
        locale = 'und-u-ks-level2',
        deterministic = false
    );
EOSQL

# Create DB for each canton to make switching easier. Those will inherit
# extensions, schemas and collations from template1 defined above.
for db in kt_schwyz kt_uri kt_bern kt_gr kt_so kt_ag kt_sg demo; do
    createdb -U "$POSTGRES_USER" "$db"
done
