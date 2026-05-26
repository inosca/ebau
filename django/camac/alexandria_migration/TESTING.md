# Alexandria Migration - Testing documentation

This is the tooling for migrating data from the old documents module into
Alexandria.

The general workflow is as follows:

1. Data from NFS / local storage is mirrored into S3 storage
   This happens via external tooling and is not covered by this module.
2. Create an Alexandria document for each documents-module "attachment",
   including versions, etc.
3. Duplicate multi-category documents in Alexandria
4. Update the links in the communications module
5. Annotate documents for fulltext indexing, thumbnails, checksums


This document mainly concerns itself with how to locally test and validate
the migration.

Check the [main readme documentation](README.md) for further information
on the procedure. 

## Configuraton

Check that the configuration is correct and complete. Specifically, ensure
the `ALEXANDRIA_*` settings, including the S3 configuration, is correct.

Additionally, if you're dealing with a large data collection, make sure the
Garage storage (in dev envs) or generally the S3 storage, has enough
capacity for running the tests. Garage by default only allows 10GB which might
not be enough.

While not in production yet, Alexandria will be disabled in the CAMAC Admin.
Be sure to un-hide the instance resource and clear the cache beforehand.

## Migration procedure

Note: The migration (and testing) utilities take an optional range of
instance IDs, so not the full database content needs to be migrated at once.


```bash
# delete all alexandria data, unlink communications attachments, drop log data
# Note: The reset doesn't take an instance range and just clears out everything
./manage.py migrate_to_alexandria reset


# Set the instance ID range to test on
FROM_INST=34000
TO_INST=35000

# Generate local data (NEVER EVER RUN THIS ANYWHERE CLOSE TO PRODUCTION!)
# This will overwrite existing documents for the given instances with test
# data. Useful if you have a prod dump but not a copy of the files themselves
./manage.py overwrite_test_documents --instances $FROM_INST..$TO_INST

# Copy data from the local (file) storage to the configured S3 bucket
# don't forget the --sync param, otherwise it will do nothing!
./manage.py sync_to_s3 --sync

# Make alexandria documents from the old documents-module
./manage.py migrate_to_alexandria  --from $FROM_INST --to $TO_INST create_documents

# Duplicate documents (Alexandria doesn't have multi-category documents, so
# they are copied into their target categories via this command)
./manage.py migrate_to_alexandria  --from $FROM_INST --to $TO_INST duplicate_documents

# Update links for the communications module
./manage.py migrate_to_alexandria  --from $FROM_INST --to $TO_INST fix_communication_links

# Update fulltext index, thumbnails, checksum for each migrated alexandria document
./manage.py migrate_to_alexandria  --from $FROM_INST --to $TO_INST annotate

# Same, but don't multi-thread. Slower, but much easier to debug
./manage.py migrate_to_alexandria --no-parallel --from $FROM_INST --to $TO_INST annotate
```

## Verification and testing

After the `duplicate_documents` stage, you can already verify that the documents exist in
Alexandria as expected, you don't need to wait for `fix_communication_links` and `annotate`
to complete.
