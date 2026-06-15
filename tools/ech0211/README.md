# eCH-0211 test scripts

A small set of Bash and Python scripts to manually test the eCH-0211 API against
a local (or remote) eBau instance. Each script logs in one or more Keycloak
clients via the `client_credentials` grant and performs a single API request,
printing the response.

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

| Script                 | Request                                                   |
| ---------------------- | --------------------------------------------------------- |
| `get-base-delivery.py` | `GET /ech/v1/application/{instance_id}` (XML)             |
| `get-categories.py`    | `GET /ech/v1/categories` (JSON:API )                      |
| `get-document.py`      | `GET /ech/v1/documents/{document_id}` (JSON:API)          |
| `get-documents.py`     | `GET /ech/v1/documents?instance={instance_id}` (JSON:API) |
| `login.py`             | `GET /api/v1/me` (JSON:API), prints user and group IDs    |

The hard-coded IDs (`instance_id`, `document_id`, ...) at the top of each script
can be adjusted to target a different dossier or document.

## Legacy Bash scripts

Most of the scripts in this directory are still legacy Bash scripts that share
`config.sh` for configuration and login. They predate the Python rewrite and are
not documented here.

The remaining Bash scripts should gradually be refactored to Python using the
helpers in `utils.py`, after which `config.sh` can be dropped in favour of
`config.toml`.

> [!tip]
> If you are reading this, please consider taking the time to refactor one (or
> more) legacy scripts.
