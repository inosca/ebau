# Alexandria Migration

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


Note: For learning how to test (locally) and verify the migration,
there's a [dedicated test guide](TESTING.md).

## Migration procedure

As outlined above, the migration procedure happens in a few distinct steps.

### NFS to S3 migration

This is the move of the bulk of all data. It will take quite a long while.

Depending on the tooling, a repeat migration can be preferrable. For example,
using something similar to `rclone` or `rsync`, a full migration can happen
while the application in its old version is still live. Once the application is
shut down for the migration, a second, "completeness" sync should run in a very
short time.


### Create Alexandria documents

For each document (or "attachment", as they're called in the old document module),
one corresponding document is created in Alexandria. For this, an explicit mapping
of categories is defined in the module's settings.

For each migration run, as well as for each document, a migration log entry is
created in the database for future examination.

### Duplicate multi-category documents

The old documents module could reference a document from multiple categories
(M:N relationship). In Alexandria, this is no longer possible.

The previous step stored all additional categories in the Alexandria document's
metadata.

This step now duplicates the documents across the categories, so each document
that was *referenced* in multiple categories is now *copied* to the same categories
in Alexandria.

Again, for each link updated, a dedicated log entry is created in the migration log
database table.

### Update communications links

The communications module can "store attachments in the documents module". This
functionality links an attachment from the communications module to a document.

Once the data has been copied to Alexandria, this step is able to update the database
references, so the communications module's attachments now point to the Alexandria
documents instead.

Same as before, for each link updated, a dedicated log entry is created in the
migration log database table.

### Annotate the documents

At this point, the migration is essentially complete, and work can continue again.

However, Alexandria has a few additional features, and works slightly differently, so
one more step is required:

* Each uploaded file can be annotated with a checksum. This can be used for verifying
  downloads and guarding against forgery, and for verifying the storage's consistency.
* Each uploaded file can be indexed, so a fulltext search can be used to find
  documents not only by title, but by content as well.
* Third, Alexandria does not calculate thumbnails as-needed, instead tries to create
  them at the time of uploading. This must now be done as well.

Note that we do only create thumbnails and fulltext index for the most recent version
of a file: Older versions usually don't need to be found, and most users will never
even try to see a thumbnail of an old document version.

Yet again, for each of these three steps, a log entry is created, so later examinations
can verify the steps have been completed for each migrated file.


## Module overview (technical)

The module consists of a Django management command that serves as the main entrypoint.

From there, work is split up into batches, then delegated to explicit migrator
classes, which each then perform the migration steps as needed. The migration commandline
is structured such that it is going thorugh each of the above steps (create
documents, duplicate, update communication links, annotate) in distinct steps as indicated
from the commandline. They are not chained automatically.

Each migrator class is designed such that it reduceds overhead as much as possible:

* Data is prefetched from the DB as much as possible to avoid any undue load on the
  DB server, speeding up the operation
* Data is inserted / updated in bulk, again to improve processing speed
* For each operation, there is a dedicated log entry that documents the success
  of the operation.


### Domain Logic -- CreateDocumentsMigrator

This migrator is the first step in the database-side migration.

* **Dependencies:** Expects that file data is already present in S3 at the paths
  stored in the old documents module.
* **Outcome:** Creates Alexandria `Document` and `File` records. Each version of
  an old attachment is converted into an Alexandria `File`. It also links
  the documents to Camac instances via `InstanceAlexandriaDocument`, and adds
   `DocumentMark` records to represent the old document-module's metainfo flags.
* **Decisions:**
    * Multi-category documents are initially created in the first category
      found. Additional categories are stored in `metainfo["duplicate-to"]` for
      later processing.
    * Uses the original attachment UUID as the Alexandria document UUID to
      maintain consistency, especially for the eCH0211 clients.
    * Fallback categories are used if the old mapping is incomplete.

### Domain Logic -- DuplicateDocumentsMigrator

This migrator handles the expansion of multi-category documents which Alexandria
doesn't support natively as M:N relationships.

* **Dependencies:** Requires `CreateDocumentsMigrator` to have run and
  populated the `duplicate-to` metadata where needed
* **Outcome:** New `Document` and `File` records for each additional category.
  Physical file copies are created in S3.
* **Decisions:**
    * Currently only supports documents with a single version. If a
      multi-category document has multiple versions, the migrator will abort
      to avoid ambiguous state.
      This is intentional, as in BE, SZ, and UR, editing (and therefore also
      versioning) is only allowed for categories/sections that disallow multi-
      category documents.

### Domain Logic -- CommunicationLinksMigrator

Updates references in the communications module to point to the new Alexandria
storage.

* **Dependencies:** Requires `CreateDocumentsMigrator` to have completed for the
  relevant instances.
* **Outcome:** `CommunicationsAttachment` records are updated to point to the
  newly created Alexandria `Document` objects.
* **Decisions:**
    * The legacy reference to the old documents module is preserved for safety
      during the transition.
      That way, we can `reset` the migration and the pointer to the original
      documents module will still be there.

### Domain Logic -- AnnotateDocumentsMigrator

Post-processing step to enable Alexandria-specific features like search and
thumbnails.

* **Dependencies:** Requires Alexandria `File` records to exist, and any
  duplication (see `DuplicateDocumentsMigrator`) to have been done where
  needed.
* **Outcome:** Updated Alexandria `File` objects with Hash calculated,
  and, where possible, fulltext/content indexed, and thumbnails generated.
* **Decisions:**
    * Uses a `ProcessPoolExecutor` to parallelize CPU-intensive tasks (especially
      Tika extraction and thumbnail generation).
    * Ensure download from S3 only happens once
    * Full-text indexing and checksums are calculated for all file versions.
    * Thumbnails are only generated for the most recent version of each
      document to save processing time and storage.
