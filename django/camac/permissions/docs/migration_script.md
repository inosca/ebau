# Migration script

There is a migration script for the permissions, named
[`migrate_permissions`](/django/camac/permissions/management/commands/migrate_permissions.py).

The purpose of the script is to take any data structure or other information
in the system and create appropriate permissions for it.

For example, users that are invited as applicants will have an entry in the
`applicants` module's database table. The old code uses these entries to determine
whether a user has applicant rights on a dossier.

The migration script creates an `InstanceACL` for every applicant, so that when
the permission module is used, the user will get the correct permissions from the
new code as well.


## Command line

The `migrate_permissions` management command provides the following options:


* `--commit`: Do commit the changes (this is opposite to the "pretent" mode used in other
  commands: Without this option, nothing is written to the DB.)
* `--check-only`: Check mode: Log a warning if a required permission is missing. NO
  change is written to the DB
* `--min-instance-id MIN_INSTANCE_ID`: Minimum instance ID to process. Defaults to zero
* `--max-instance-id MAX_INSTANCE_ID`: Maximum instance ID to process. Defaults to the maximum instance id

The `--min-instance-id` and `--max-instance-id` are useful for devleopment, testing, or
correcton of production issues: It allows users to provide a range of instance IDs; only
these instances (dossiers) will be checked / updated instead of the whole database. 

## Inner workings

The migration script works as follows:

* From the application state, a set of "expected" or "needed" ACLs is created
  (A). These stem from various information in the database, such as applicants,
  lead municipality, any assigned work items etc.
* Additionally, all existing InstanceACLs are read into a similer data structure
  (B).
* Then the two sets are compared:
  - Any ACL that exists in the (A) set that are missing in set (B) need to
    be created
  - Any ACL that exists in the (B) set that are missing in set (A) need to
    be removed / revoked.

This algorithm allows an efficient migration, as only the minimum set of changes 
need to be applied to the database. It is however relatively memory-hungry.
