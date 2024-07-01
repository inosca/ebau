#!/bin/bash
set -e

psql -d template1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE EXTENSION citext;
    CREATE EXTENSION hstore;
    CREATE EXTENSION "uuid-ossp";
EOSQL

# The case insensitive collation must be created in the template DB for the
# testing environments to work as they don't run the regular django migrations
# in order to speed up the testing setup. Normally, this django migration would
# create that collation: django/camac/core/migrations/0109_case_insensitive_collation.py
#
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

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE kt_schwyz;
    GRANT ALL PRIVILEGES ON DATABASE kt_schwyz TO $POSTGRES_USER;
    CREATE DATABASE kt_uri;
    GRANT ALL PRIVILEGES ON DATABASE kt_uri TO $POSTGRES_USER;
    CREATE DATABASE kt_bern;
    GRANT ALL PRIVILEGES ON DATABASE kt_bern TO $POSTGRES_USER;
    CREATE DATABASE demo;
    GRANT ALL PRIVILEGES ON DATABASE demo TO $POSTGRES_USER;
    CREATE DATABASE kt_gr;
    GRANT ALL PRIVILEGES ON DATABASE kt_gr TO $POSTGRES_USER;
    CREATE DATABASE kt_so;
    GRANT ALL PRIVILEGES ON DATABASE kt_so TO $POSTGRES_USER;
    CREATE DATABASE metabase;
    GRANT ALL PRIVILEGES ON DATABASE metabase TO $POSTGRES_USER;
    \c kt_uri;
    CREATE SCHEMA keycloak AUTHORIZATION $POSTGRES_USER;
    \c kt_bern;
    CREATE SCHEMA keycloak AUTHORIZATION $POSTGRES_USER;
    \c kt_gr;
    CREATE SCHEMA keycloak AUTHORIZATION $POSTGRES_USER;
    \c kt_so;
    CREATE SCHEMA keycloak AUTHORIZATION $POSTGRES_USER;
    \c demo;
    CREATE SCHEMA keycloak AUTHORIZATION $POSTGRES_USER;
EOSQL
