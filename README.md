# ebau

Electronic building permit application for swiss cantons.

## Table of Content

- [ebau](#ebau)
  - [Table of Content](#table-of-content)
  - [Requirements](#requirements)
  - [Development](#development)
    - [Basic setup](#basic-setup)
    - [Working locally with django](#working-locally-with-django)
      - [Debugging](#debugging)
    - [Working locally with ember](#working-locally-with-ember)
      - [Yarn workspace](#yarn-workspace)
    - [GWR API](#gwr-api)
        - [Django profiling](#django-profiling)
        - [Visual Studio Code](#visual-studio-code)
    - [Predefined credentials](#predefined-credentials)
    - [Customize api](#customize-api)
  - [Sending email](#sending-email)

## Requirements

The preferred development environment is based on Docker.

- Docker >= 20.04
- Docker-Compose

For local development:

Python:

- python 3.8
- pyenv/virtualenv

Ember:

- current LTS of Node.js
- yarn

## Development

### Basic setup

In general Docker can be used to get ebau up and running quickly. Simply
set `APPLICATION` to the project you want to work on.

```bash
# choose what project you want to start
# also set this when developing locally
export APPLICATION={kt_schwyz|kt_uri|kt_bern|demo}
# setup hostnames, only needed once
echo "127.0.0.1 camac-ng-portal.local camac-ng.local camac-ng-keycloak.local caluma-portal.local" | sudo tee -a /etc/hosts
# needed for permission handling, only needs to be run once
echo UID=$UID > .env
# set application-specific .env variables
make $APPLICATION

# finally build images
docker-compose up -d --build

# load initial config
## if APPLICATION is kt_schwyz
make loadconfig-camac

## else
make loadconfig

```

For automatic checks during commit (formatting, linting) you can setup a git hook with the following commands:

```bash
pip install pre-commit
pre-commit install
```

### Working locally with django

```bash
docker-compose up -d django
cd django
export APPLICATION={kt_schwyz|kt_uri|kt_bern|demo}  # Also set this when developing locally
export APPLICATION_ENV=local
export VISIBILITY_CLASSES=camac.caluma.extensions.visibilities.CustomVisibility
export PERMISSION_CLASSES=camac.caluma.extensions.permissions.CustomPermission
export VALIDATION_CLASSES=camac.caluma.extensions.validations.CustomValidation
export DATA_SOURCE_CLASSES=camac.caluma.extensions.data_sources.Municipalities,camac.caluma.extensions.data_sources.Services
# Create virtualenv for camac with Python 3.8 - `pyenv virtualenv 3.8.x ebau` or similar
# Install python dependencies
make install-dev
# Load configuration
./manage.py camac_load
# some functionality need unoconv to run
docker-compose --file compose/ci.yml up -d unoconv
pytest  # run tests
```

#### Debugging

For debugging inside container shell, use this:

```bash
make debug-django
```

### Working locally with ember

```bash
docker-compose up -d --build db django
cd {ember|ember-camac-ng|ember-caluma-portal|ember-ebau} # Enter ember from the top level of the repo
yarn # Install dependencies
yarn test # Run tests
yarn start-proxy # Run dev server with proxy to django api
```

#### Yarn workspace

Note however that those two apps `ember-caluma-portal` and `ember-camac-ng` share the same node modules tree through a [yarn workspace](https://classic.yarnpkg.com/en/docs/workspaces/).

The common yarn workspace allows us to share code (e.g. addons) between the apps which are part of this repo (instead of following the typical approach of publishing releases on npm). This also means that

- (+) we save some disk space because of the avoided duplication in the `node_modules` directory
- (-) the docker build processes of the two frontend containers have to run in the context of the root of the repo, in order to access the shared dependencies during build time
- (-) the ember versions `ember-caluma-portal` and `ember-camac-ng` need to be kept in sync

### GWR API

If you use the GWR module, you need to generate a Fernet key
according to the [documentation](https://github.com/adfinis-sygroup/ebau-gwr) of the gwr backend.

You need to set this key in each environment/server in your env file.
**Generate a seperate key for each environment since this is used to store /
read the gwr user passwords.**

##### Django profiling

To enable `django-silk` for profiling, simply add `DJANGO_ENABLE_SILK=True`
to your `django/.env` file. Then restart the django container and browse to
http://camac-ng.local/api/silk/.

##### Visual Studio Code

The remote debugger settings for VS Code are committed to the repository.

- The configuration file is located at `.vscode/launch.json`.
- The keyboard shortcut to launch the debugger is <kbd>F5</kbd>.
- [Information on VS Code debugging](https://code.visualstudio.com/docs/editor/debugging)

To enable debugging in the django container the ptvsd server must be started.
Since this debug server collides with other setups (PyCharm, PyDev) it will
only be started if the env var `ENABLE_PTVSD_DEBUGGER` is set to `True` in
[`django/.env`](django/.env).

### Predefined credentials

The following administator accounts are present in Keycloak or the DB,
respectively:

| _Application_ | _Role_      | _Username_ | _Password_ | _Notes_ |
| ------------- | ----------- | ---------- | ---------- | ------- |
| kt_schwyz     | Admin       | admin      | admin      |         |
|               | Publikation | adsy       | adsy       |         |
| kt_uri        | Admin       | admin      | admin      |         |
|               | PortalUser  | portal     | portal     |         |
| kt_bern       | Admin       | user       | user       |         |

### Customize api

The api should be designed the way that it can be used by any ebau project. For needed
customization following rules apply:

- each permission may be mapped to a specific role in the specific project.
  In case a role may have different set of permissions than already available,
  introduce a new one and adjust the different views accordingly.
- for features which may not be covered by permissions, introduce feature flags.

For different feature flags and permissions see `APPLICATIONS` in settings.py.

## Sending email

In development mode, the application is configured to send all email to a
Mailhog instance, so unless you specify something else, no email will be
sent out from the development environment.

You can access the Mailhog via http://camac-ng.local/mailhog . Any email sent out
will be instantly visible there.