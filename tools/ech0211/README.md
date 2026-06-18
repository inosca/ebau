# eCH-0211 test scripts

A small set of Python scripts to manually test the eCH-0211 API against a local
(or remote) eBau instance. Each script logs in one or more Keycloak clients via
the `client_credentials` grant and performs a single API request, printing the
response.

## Setup

The Python scripts only depend on `requests` (and the standard library
`tomllib`, which ships with Python 3.11+):

```bash
pipx install requests
```

Copy the example config and adapt it to your environment:

```bash
cp config.example.toml config.toml
```

```toml
[ech0211]
endpoint = "http://ember-ebau.localhost"

[auth]
endpoint = "http://ebau-keycloak.localhost"
group_id = 10035

[[auth.clients]]
id = "ech-client"
secret = "your-client-secret"

# [[auth.clients]]
# id = "gemeinde-davos"
# secret = "another-secret"
```

- `ech0211.endpoint` base URL of the eCH-0211 API.
- `auth.endpoint` base URL of Keycloak.
- `auth.group_id` value sent as the `x-camac-group` header.
- `auth.clients` one `[[auth.clients]]` table per client (`id` + `secret`).
  Every request is executed once per configured client.

> [!note]
> `config.toml` holds your secrets and is git-ignored. Keep
> `config.example.toml` up to date when the config format changes.

## Usage

Run any of the scripts from this directory (so that `config.toml` is found):

```bash
./get-documents.py
```

| Script                           | Request                                                           |
| -------------------------------- | ----------------------------------------------------------------- |
| `delete-document-decision.py`    | `DELETE /ech/v1/documents/{document_uuid}/decision`               |
| `delete-document-publication.py` | `DELETE /ech/v1/documents/{document_uuid}/publication`            |
| `delete-document-sensitive.py`   | `DELETE /ech/v1/documents/{document_uuid}/sensitive`              |
| `delete-document-void.py`        | `DELETE /ech/v1/documents/{document_uuid}/void`                   |
| `delete-document.py`             | `DELETE /ech/v1/documents/{document_uuid}`                        |
| `delete-file.py`                 | `DELETE /ech/v1/files/{file_uuid}`                                |
| `get-base-delivery.py`           | `GET /ech/v1/application/{instance_id}`                           |
| `get-categories.py`              | `GET /ech/v1/categories`                                          |
| `get-document.py`                | `GET /ech/v1/documents/{document_uuid}`                           |
| `get-documents.py`               | `GET /ech/v1/documents?instance={instance_id}`                    |
| `get-file.py`                    | `GET /ech/v1/files/{file_uuid}`                                   |
| `get-message.py`                 | `GET /ech/v1/message/?last={message_id}`                          |
| `login.py`                       | `GET /api/v1/me`                                                  |
| `patch-document-update.py`       | `PATCH /ech/v1/documents/{document_uuid}`                         |
| `post-accompanying-report.py`    | `POST /ech/v1/send/` (`eventAccompanyingReport`)                  |
| `post-change-responsibility.py`  | `POST /ech/v1/send/` (`eventChangeResponsibility`)                |
| `post-claim.py`                  | `POST /ech/v1/send/` (`eventRequest`, claim)                      |
| `post-close-dossier.py`          | `POST /ech/v1/send/` (`eventCloseArchiveDossier`)                 |
| `post-document-decision.py`      | `POST /ech/v1/documents/{document_uuid}/decision`                 |
| `post-document-publication.py`   | `POST /ech/v1/documents/{document_uuid}/publication`              |
| `post-document-sensitive.py`     | `POST /ech/v1/documents/{document_uuid}/sensitive`                |
| `post-document-void.py`          | `POST /ech/v1/documents/{document_uuid}/void`                     |
| `post-file.py`                   | `POST /ech/v1/files`                                              |
| `post-inquiry.py`                | `POST /ech/v1/send/` (`eventRequest`, inquiry)                    |
| `post-notice-ruling.py`          | `POST /ech/v1/send/` (`eventNotice`)                              |
| `post-submit.py`                 | `POST /ech/v1/send/` (`eventSubmitPlanningPermissionApplication`) |
| `post-task.py`                   | `POST /ech/v1/send/` (`eventRequest`, task)                       |

The hard-coded IDs (`instance_id`, `document_id`, ...) at the top of each script
are set up for the GR dev dataset and should work out of the box there. If you
target a different environment or dataset, adjust them to a matching dossier,
document, ...
