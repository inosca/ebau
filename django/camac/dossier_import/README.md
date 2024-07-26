# Import Dossiers

## Configuration

Dossiers can be imported from ZIP Archives holding metadata on dossiers as well as one directory for each dossier.
Import is specific to configuration. Available configurations can be found in `./camac/dossier_import/config`.

The import can be configured in `django/camac/settings/modules/dossier_import.py` in the section of the application in question.

```python
DOSSIER_IMPORT = {
    'your-config': {
        "ENABLED": True,  # Switch it on.
        # reference your writer class in `dossier_import/config/<your_config>.py` that implements handling of
        # the imported dossier according to the config's requirements. See doc string of the base class
        # "camac.dossier_import.writer.DossierWriter"
        "WRITER_CLASS": "camac.dossier_import.config.<config_name>.<ConfigWriterClass>",
        # Map target import states to the InstanceState IDs of your config. workflow and edgecases
        # Supported states are: SUBMITTED, APPROVED, DONE, WRITTEN OFF .. but extensible by config
        "INSTANCE_STATE_MAPPING": {},  # e. g. {"SUBMITTED": 2, "APPROVED": 8, "DONE": 10},
        # The user doing the import. Defaults to `service-account-camac-admin`
        "USER": "service-account-camac-admin",
        "GROUP_ID": 1,  # Group with service_id and this role_id is created Instances' group
        "FORM_ID": 1,  # "migriertes-dossier"
        "CALUMA_FORM": "baugesuch",  # "dummy"-Form when importing for Kt. Schwyz
        "ATTACHMENT_SECTION_ID": 1,  # attachmentsection for imported documents
        # The default coordinate projection is for Switzerland/Lichtenstein epsg:2056
        # Set to a different projection if transformation is required.
        # See https://epsg.io/ for reference
        #"TRANSFORM_COORDINATE_SYSTEM": "epsg:4326",  # use world wide coordinates instead of swiss ones
        # Set required values for transfering an import to the production system
        "PROD_URL": env.str("DJANGO_DOSSIER_IMPORT_PROD_URL"),
        "PROD_AUTH_URL": env.str("DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL"),
        "PROD_SUPPORT_GROUP_ID": 486,
        # That's required for `reversing` the URL to the dossier-import resource tab in the UI
        # for legacy camac deployments (PHP)
        "RESOURCE_ID_PATH": "/index/template/resource-id/25#/dossier-import/",
        },
    }
}
```

## Testing validity

Validity testing is done comparing imported data with the output of the `camac.instance.master_data.MasterData` instance.
So make sure that the 'MASTER_DATA' config in `settings_master_data.py` has all datapoints that are imported configured.
Pay extra attention to compound datapoints like persons and plot_data.

## Formal validation

The archive and metadata need to comply to a predefined structure (directory naming and
columns and data types respectively).

Importing dossiers is for one group/location (aka Municipality) at a time and therefore requires
parametrization for

- camac-user
- group owning the dossiers
- the location the dossiers will be assigned to

Attachments are imported from the directories if and only if identified by `python-magic`.

The `import_dossier` app provides two variants for importing via a django management command.

### Variant 1: backend cli

1. upload the archive e. g. archive location: `/data/archive.zip` and make it available within the container:

```bash
docker cp /data/archive.zip $(docker compose ps -q django):/app/archive.zip
```

2. make sure all the objects your're referencing with ids exist in your setup and start the import:

```bash
docker-compose exec django python manage.py import_dossiers from_archive --user_id=7 --group_id=13 --location_id=666 archive.zip
```

Note: atm there is no feedback during the import. An import can take quite some time (roughly a bit under 10mins/1000)

### Variant 2: ZIP archive is uploaded and verified via REST api / frontend

1. Upload the archive to `/api/v1/dossier-imports`

   - `source file` MUST be smaller than 1GB
   - set `location_id` in the multipart when uploading the file (as opposed to resource object)

2. Make sure there are no validation errors (the file would be removed and cannot be imported) resulting in a ValueError
   informing you that no file is associated with the source_file.

3. To perform the actual import POST to `/api/v1/dossier-imports/<UUID>/start`

4. run command in backend:

```bash
docker-compose exec django python manage.py import_dossiers from_session 12345678-90ab-cdef-ba09-87654321 [--location_id=13]
```

## Debugging Dossier Imports

In order to debug the domain-logic functions that are called by the respective actions on import you need to run the `async_tasks`
in the same process as the request is processed.

This can be achieved by settings the environment variable `DJANGO_Q_ENABLE_SYNC=true` and attaching to the django container or running tests.
You may now set breakpoints in the scope of those functions and get dropped to a pdb shell (this requires that the container is run with the
options `tty` and `stdin_open` (docker run flags `-ti`).

`docker compose attach django`

In order to maintain consistency with testing async_tasks `Q_CLUSTER['sync']` is set to false for tests
in pytest's `ini_options.env` so changing the environment for developping and debugging will not mess with tests.

The code triggering async_tasks will schedule the task but not actually run the test due to tests running
in a transaction.

You can't override `settings.Q_CLUSTER['sync']` in fixtures or testfunctions at will. It won't be effective for activating
sync mode for tests. If you want tests to run in sync mode, you need to change the setting in `django/pyproject.toml`.
NOTE: Calling the task at the call site with `async_task(sync=True)` does not run the task in sync mode (according to the docs
it "simulates" task execution).
