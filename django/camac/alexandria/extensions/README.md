# Visibilities and Permissions

**ATTENTION: configuration is case sensitive!**

## Overview
We have a special system that handles visibility and permissions of documents and files.
The others models (tags, etc.) are not configurable like that.

To define visibilities and permissions for documents (and files), create an `access` object in
the `metainfo` property of any category model. Each role has to be configured into the `access`
to have visibility and permissions.
If a role is not in the `access` object it will not even see the category.

Checkout the example below for an example configuration.

## `visibility`
Visibilities determines what users can see. Visibilities also get evaluated before a permission check.

- `all`: No restriction
- `service`: Only users which are in the same service as the service set in `created_by_group`
    - `created_by_group` is set automatically with the service of the user who created the document.

## `permissions`
`permissions` determine what users can do with the document.
They are split into the three main request types:

- **`create`**: `POST`, Users can create.
- **`update`**: `PATCH`, Users can modify.
- **`delete`**: `DELETE`, Users can delete.

Each permission type must be configured independently in a list.
Multiple of the same types will chained with an `OR`.

If you want to define "read only" permissions, leave out the `permission` key.

Furthermore, a permission can be narrowed down even more with the following options:

### `fields`
Fields restrict which fields of the model are modifiable.
By leaving out the `fields` option, all fields are counted as modifiable.
`fields` only apply to `create` and `update` permissions.

Configure by setting a list of the fields which should be modifiable.
Available options are in [settings](../../settings_alexandria.py) under the key `RESTRICTED_FIELDS`.
Current list of fields:
```py
"title",
"description",
"metainfo",
"category",
"tags",
"marks",
"files",
```

The `files` field is a little special as this also controls the file model permission.
That means if you want to allow the creation of a file you will need to set `files` in `fields`

- `create`: any request data containing fields not listed in the `fields` array will be rejected.
- `update`: any request that attempts to change fields not present in the `fields` array will be rejected.

### `scope`
Scopes restrict who can edit the document.
`scope` only applies to `update` and `delete`.

- `All`: no restriction
- `Service`:  Only users which are in the same service as the service set in `created_by_group`.

Scopes are defined in [scopes.py](permissions/scopes.py) as classes. The configured scope must match the class name.

### `condition`
A permission can be conditional, which means only if the condition is met, the action (e.g. `create`) can be done.

- `InstanceState`: Check if the instance is in the defined states (string or list, e.g `["new"]`).
- `PaperInstance`: Check if `CalumaApi().is_paper` evaluates to true.
- `ReadyWorkItem`: Check if a `READY` work item with the given `task_id` is found in the case family of the instance.
    - Special case for `additional-demand`, as we only check on a specific child case defined by `caluma-document-id`
    - More special cases can be implemented by creating a function, to get the work item which has to be checked, in the format `get_{task_id}`.

Conditions are defined in [conditions.py](permissions/conditions.py) as classes. The configured conditions must match the class name.

## Example
Check out the existing configuration in [kt_gr](../../../kt_gr/config/alexandria_core.json)

Below a configuration is explained in full sentences.
```json
"metainfo": {
    "access": {
        "support": {
            "visibility": "all",
            "permissions": [
                {
                    "permission": "create"
                },
                {
                    "scope": "All",
                    "permission": "update"
                },
                {
                    "scope": "All",
                    "permission": "delete"
                }
            ]
        },
        "applicant": {
            "visibility": "all",
            "permissions": [
                {
                    "fields": ["metainfo", "title", "category", "files"],
                    "condition": {
                        "InstanceState": "new"
                    },
                    "permission": "create"
                },
                {
                    "scope": "All",
                    "condition": {
                        "InstanceState": "new"
                    },
                    "permission": "delete"
                }
            ]
        },
        "service-lead": {
            "visibility": "service",
            "permissions": [
              {
                "permission": "create"
              },
              {
                "scope": "Service",
                "permission": "update"
              }
            ]
        }
    }
}
```

What does this configuration mean?

Users with the role:
- `support`
    - can see everything
    - can modify (`create`, `update`, `delete`) everything without restrictions
- `applicant`
    - can see everything
    - can create documents only with the fields `metainfo`, `title`, `category` and also create files, but only while the instance state is `new`.
    - can delete, but only while the instance state is `new`.
- `service-lead`
    - can see only what was created by the same service
    - can create without restrictions
    - can only update documents created by the same service
