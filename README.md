# eBau

Electronic building permit application for Swiss cantons.

## Table of Contents

<!-- vim-markdown-toc GFM -->

- [Overview](#overview)
  - [Folder structure](#folder-structure)
  - [Modules](#modules)
- [Requirements](#requirements)
- [Development](#development)
  - [Basic setup](#basic-setup)
  - [Predefined credentials](#predefined-credentials)
    - [Debugging](#debugging)
  - [Working locally with ember](#working-locally-with-ember)
    - [Yarn workspace](#yarn-workspace)
  - [GWR API](#gwr-api)
    - [Django profiling](#django-profiling)
    - [Visual Studio Code](#visual-studio-code)
  - [Customize API](#customize-api)
- [Sending email](#sending-email)
- [License](#license)

<!-- vim-markdown-toc -->

## Overview

This repository contains the source code for the web applications used to handle electronic building permits and comparable processes in the Swiss cantons of Berne, Schwyz and Uri. The software stack is undergoing a "rolling" modernization process, meaning that the application is built up on multiple technology stacks. The evolution of the framework happened in roughly the following stages:

1. Base: PHP-based, server-side rendered (legacy, not part of this repository)
2. a) Introduction of Django (Python)-based model layer, allowing for simpler database management and development of REST APIs,
   b) Introduction of Vue.js-based frontend modules that interact with REST APIs, embedded in legacy app
3. Introduction of Ember.js-based "portal" for submitting forms, also based on REST APIs
4. Introduction of [Caluma](https://github.com/projectcaluma/caluma) as form- and workflow-engine
5. Embedding of Ember.js-based modules (replacing Vue.js), styled using [UIkit](https://getuikit.com/)
6. Replacing the legacy application frame by an Ember.js app (ember-ebau)

The following image shows a high-level overview of the current architecture:

![Architecture](https://i.imgur.com/dZseZU5.jpg)

While technically only one database is used, two are shown in the diagram to highlight that Caluma is using its own schema, while the legacy app and bridge API share a common schema.

### Folder structure

```
├── compose                # docker-compose files
├── db                     # database Dockerfile and utils
├── django                 # backend code, containing both Bridge API and Caluma
├── document-merge-service # document generation templates and config
├── ember                  # Ember.js based portal using REST API, precursor of `ember-caluma-portal`
├── ember-caluma-portal    # Caluma-based portal
├── ember-camac-ng         # Ember.js modules used in internal area
├── ember-ebau             # New application container for internal area
├── ember-ebau-core        # Ember.js addon for code sharing between multiple Ember.js apps
├── keycloak               # Keycloak configuration for local development
├── proxy                  # Nginx configuration for local development
└── tools                  # miscellaneous utilities
```

### Modules

The following table lists the most important modules in the "internal" part of the application and their respective progress in the modernization based on four steps:

1. **JS / API-driven**: frontend is based on Vue.js, backend is a REST or GraphQL API
2. **Ember.js**: frontend is implemented with Ember.js
3. **UIkit**: styling is implemented using UIkit
4. **Part of ember-ebau**: this module has been integrated in ember-ebau

| Module                       | Description                              | JS / API-driven    | Ember.js           | UIkit              | Part of ember-ebau |
| ---------------------------- | ---------------------------------------- | ------------------ | ------------------ | ------------------ | ------------------ |
| _Main Nav (resource)_        |                                          |                    |                    |                    |                    |
| Dossier list                 | Show a list of dossiers                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Task list                    | Show a list of tasks                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| Organization                 | Manage details of own organization       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| Static content               | Static content, markdown editor          | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Text components              | Manage snippets for usage in text fields | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Templates                    | Manage document templates (docx)         | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Permissions                  | Decentralized permission management      | :x:                | :x:                | :x:                | :x:                |
| _Subnav (instance resource)_ |                                          |                    |                    |                    |                    |
| Tasks                        | View and manage tasks                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Form                         | View and edit main form                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Journal                      | Collaborative notebook                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Responsible                  | Assign responsible users                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| Audit                        | Perform structured audit                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| Publication                  | Manage publication in newspaper          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| History                      | Shows milestones and historical data     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                |
| Documents [1]                | Document management                      | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Audit-Log                    | Shows form changes                       | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Template                     | Generate document from template          | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Claims                       | Ask applicant for additional info        | :heavy_check_mark: | :x:                | :x:                | :x:                |
| Billing                      | Manage handling fees                     | :x:                | :x:                | :x:                | :x:                |
| Circulation [2]              | Get feedback from other organizations    | :x:                | :x:                | :x:                | :x:                |

[1] To be replaced with [alexandria](https://github.com/projectcaluma/alexandria).
[2] To be replaced with [the distribution package in ember-caluma](https://github.com/projectcaluma/ember-caluma/tree/main/packages/distribution).

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

Docker can be used to get eBau up and running quickly. Simply run the following script.

```bash
make start-dev-env
```

In case you want to manually modify /etc/hosts following domains need to point to
127.0.0.1 (localhost):

```
ebau-portal.local ebau.local ebau-keycloak.local ebau-rest-portal.local
```

For automatic checks during commit (formatting, linting) you can setup a git hook with the following commands:

```bash
pip install pre-commit
pre-commit install
```

After, you should be able to use to the following services:

- [ember-ebau.local](http://ember-ebau.local) - new main application used for "internal" users
- [ebau-portal.local](http://ebau-portal.local) - public-facing portal (Caluma-based, default choice for new projects, used in Kt. BE, UR)
- [ebau-rest-portal.local](http://ebau-rest-portal.local) - public-facing portal (REST-API-based, precursor of the Caluma-based portal, used in Kt. SZ)
- [ebau.local/django-admin/](http://ebau.local/django-admin/) - Django admin interface
- [ebau-keycloak.local/auth](http://ebau-keycloak.local/auth) - IAM solution

### Predefined credentials

The following administrator accounts are present in Keycloak or the DB,
respectively:

| _Application_ | _Role_      | _Username_ | _Password_ | _Notes_ |
| ------------- | ----------- | ---------- | ---------- | ------- |
| kt_schwyz     | Admin       | admin      | admin      |         |
|               | Publikation | adsy       | adsy       |         |
| kt_uri        | Admin       | admin      | admin      |         |
|               | PortalUser  | portal     | portal     |         |
| kt_bern       | Admin       | user       | user       |         |

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
**Generate a separate key for each environment, since this is used to store /
read the gwr user passwords.**

##### Django profiling

To enable `django-silk` for profiling, simply add `DJANGO_ENABLE_SILK=True`
to your `django/.env` file. Then restart the django container and browse to
http://ebau.local/api/silk/.

##### Visual Studio Code

The remote debugger settings for VS Code are committed to the repository.

- The configuration file is located at `.vscode/launch.json`.
- The keyboard shortcut to launch the debugger is <kbd>F5</kbd>.
- [Information on VS Code debugging](https://code.visualstudio.com/docs/editor/debugging)

To enable debugging in the django container the ptvsd server must be started.
Since this debug server collides with other setups (PyCharm, PyDev) it will
only be started if the env var `ENABLE_PTVSD_DEBUGGER` is set to `True` in
[`django/.env`](django/.env).

### Customize API

The API should be designed in a way, that allows it to be used by any eBau project. For needed
customization, the following rules apply:

- each permission may be mapped to a specific role in the specific project.
  In case a role may have different set of permissions than already available,
  introduce a new one and adjust the different views accordingly.
- for features which may not be covered by permissions, introduce feature flags.

For different feature flags and permissions, see `APPLICATIONS` in settings.py.

## Sending email

In development mode, the application is configured to send all email to a
Mailhog instance, so unless you specify something else, no email will be
sent out from the development environment.

You can access the Mailhog via http://ebau.local/mailhog . Any email sent out
will be instantly visible there.

## License

This project is licensed under the EUPL-1.2-or-later. See [LICENSE](./LICENSE) for details.
