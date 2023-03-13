<img src="https://user-images.githubusercontent.com/7962156/203104928-1dda9728-54e2-4c72-8afd-f0bec914d8d2.svg" alt="inosca/ebau logo" width="200" />

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
  - [Django profiling](#django-profiling)
  - [Visual Studio Code](#visual-studio-code)
  - [GWR API](#gwr-api)
  - [Customize API](#customize-api)
  - [Sending email](#sending-email)
- [License](#license)

<!-- vim-markdown-toc -->

## Overview

This repository contains the source code for the web applications used to handle electronic building permits and comparable processes in the Swiss cantons of Berne, Schwyz and Uri.

The following image shows a high-level overview of the architecture:

<img src="https://i.imgur.com/CjDwlsL.jpg" alt="Architecture" width="500" />

- The application is composed of various Docker containers, which are shown in light blue in the architecture overview.
- The frontend consists of two Ember.js apps, one for applicants submitting building permit applications ("portal"), and another used by members of the public authorities ("internal area"). The two apps can share code through the Ember Addon `ember-ebau-core`.
- The backend is based on Python/Django and exposes a GraphQL API for forms and workflows based on [Caluma](https://caluma.io) and set of domain-specific REST endpoints ([Django REST Framework](https://www.django-rest-framework.org/)).
- PostgreSQL is used as database.

### Folder structure

```
├── compose                # docker-compose files
├── db                     # database Dockerfile and utils
├── django                 # backend code, containing both API and Caluma
├── document-merge-service # document generation templates and config
├── ember-caluma-portal    # Caluma-based portal
├── ember-camac-ng         # Ember.js app optimized for embedding in other applications
├── ember-ebau             # Ember.js based application for internal area
├── ember-ebau-core        # Ember.js addon for code sharing between multiple Ember.js apps
├── keycloak               # Keycloak configuration for local development
├── proxy                  # Nginx configuration for local development
└── tools                  # miscellaneous utilities
```

### Modules

Due to ongoing modernization work, some Frontend modules are not yet integrated in `ember-ebau`, but instead are still part of `ember-camac-ng`. Few Frontend modules are not part of this repository yet at all. The following table lists the most important modules in the "internal" part of the application and their respective completeness / integration state (in the `demo` configuration).

| Module                       | Description                              | Backend            | Frontend                 | Part of ember-ebau       |
| ---------------------------- | ---------------------------------------- | ------------------ | ------------------------ | ------------------------ |
| _Main Nav (resource)_        |                                          |                    |                          |                          |
| Dossier list                 | Show a list of dossiers                  | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Task list                    | Show a list of tasks                     | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Templates                    | Manage document templates (docx)         | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Organization                 | Manage details of own organization       | :heavy_check_mark: | :heavy_check_mark:       | :hourglass_flowing_sand: |
| Static content               | Static content, markdown editor          | :heavy_check_mark: | :hourglass_flowing_sand: | :hourglass_flowing_sand: |
| Text components              | Manage snippets for usage in text fields | :heavy_check_mark: | :hourglass_flowing_sand: | :hourglass_flowing_sand: |
| _Subnav (instance resource)_ |                                          |                    |                          |                          |
| Tasks                        | View and manage tasks                    | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Form                         | View and edit main form                  | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Distribution                 | Get feedback from other organizations    | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Alexandria                   | Document management                      | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Template                     | Generate document from template          | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Journal                      | Collaborative notebook                   | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| History                      | Shows milestones and historical data     | :heavy_check_mark: | :heavy_check_mark:       | :heavy_check_mark:       |
| Responsible                  | Assign responsible users                 | :heavy_check_mark: | :heavy_check_mark:       | :hourglass_flowing_sand: |
| Audit                        | Perform structured audit                 | :heavy_check_mark: | :heavy_check_mark:       | :hourglass_flowing_sand: |
| Publication                  | Manage publication in newspaper          | :heavy_check_mark: | :heavy_check_mark:       | :hourglass_flowing_sand: |
| Audit-Log                    | Shows form changes                       | :heavy_check_mark: | :hourglass_flowing_sand: | :hourglass_flowing_sand: |
| Claims                       | Ask applicant for additional info        | :heavy_check_mark: | :hourglass_flowing_sand: | :hourglass_flowing_sand: |

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

Docker can be used to get eBau up and running quickly. The following script guides you through the setup process. We recommend using the `demo` config for now, since it features the highest number of modules in the `ember-ebau` app.

```bash
make start-dev-env
```

In case you want to manually modify /etc/hosts following domains need to point to
127.0.0.1 (localhost):

```
ebau-portal.local ebau.local ebau-keycloak.local ember-ebau.local ebau-rest-portal.local
```

For automatic checks during commit (formatting, linting) you can setup a git hook with the following commands:

```bash
pip install pre-commit
pre-commit install
```

After, you should be able to use to the following services:

- [ember-ebau.local](http://ember-ebau.local) - new main application used for "internal" users
- [ebau-portal.local](http://ebau-portal.local) - public-facing portal (Caluma-based, default choice for new projects, used in Kt. BE, UR)
- [ebau.local/django/admin/](http://ebau.local/django/admin/) - Django admin interface
- [ebau-keycloak.local/auth](http://ebau-keycloak.local/auth) - IAM solution

### Predefined credentials

The following administrator accounts are present in Keycloak or the DB,
respectively:

| _Application_ | _Role_      | _Username_ | _Password_ | _Notes_ |
| ------------- | ----------- | ---------- | ---------- | ------- |
| demo          | Admin       | user       | user       |         |
| kt_schwyz     | Admin       | admin      | admin      |         |
|               | Publikation | adsy       | adsy       |         |
| kt_uri        | Admin       | admin      | admin      |         |
|               | PortalUser  | portal     | portal     |         |
| kt_bern       | Admin       | user       | user       |         |

### Debugging

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

### Django profiling

To enable `django-silk` for profiling, simply add `DJANGO_ENABLE_SILK=True`
to your `django/.env` file. Then restart the django container and browse to
http://ebau.local/api/silk/.

### Switching tenant

To switch from the `demo` config to `kt_bern`, one has to make sure that the frontend apps take up the right 
environment variables.

#### Working locally with ember

1. Stop the frontend servers started with `yarn start-proxy`
2. Run `make kt_bern`
3. Run `docker-compose up -d && make loadconfig`
4. Start using command from step 1

#### Working with docker only

1. Run `docker-compose down`
2. Run `make kt_bern`
3. Run `docker-compose build`
4. Run `docker-compose up -d`

### Visual Studio Code

The remote debugger settings for VS Code are committed to the repository.

- The configuration file is located at `.vscode/launch.json`.
- The keyboard shortcut to launch the debugger is <kbd>F5</kbd>.
- [Information on VS Code debugging](https://code.visualstudio.com/docs/editor/debugging)

To enable debugging in the django container the ptvsd server must be started.
Since this debug server collides with other setups (PyCharm, PyDev) it will
only be started if the env var `ENABLE_PTVSD_DEBUGGER` is set to `True` in
[`django/.env`](django/.env).

### GraphQl

In order to talk to the graphql endpoint with authentication, you can install 
a GraphQL Tool (much like Postman). Things you might consider here:

- [Insomnia](https://insomnia.rest/download)
- [Altair GraphQL client](https://altairgraphql.dev/#download)

### GWR API

The GWR module is developed in two separate repositories:

- Frontend: [inosca/ember-ebau-gwr](https://github.com/inosca/ember-ebau-gwr)
- Backend: [inosca/ebau-gwr](https://github.com/inosca/ebau-gwr)

If you use the GWR module, you need to generate a Fernet key
according to the [documentation](https://github.com/inosca/ebau-gwr) of the gwr backend.

You need to set this key in each environment/server in your env file.
**Generate a separate key for each environment, since this is used to store /
read the gwr user passwords.**

### Customize API

The API should be designed in a way, that allows it to be used by any eBau project. For needed
customization, the following rules apply:

- each permission may be mapped to a specific role in the specific project.
  In case a role may have different set of permissions than already available,
  introduce a new one and adjust the different views accordingly.
- for features which may not be covered by permissions, introduce feature flags.

For different feature flags and permissions, see `APPLICATIONS` in settings.py.

### Sending email

In development mode, the application is configured to send all email to a
Mailhog instance, so unless you specify something else, no email will be
sent out from the development environment.

You can access the Mailhog via http://ebau.local/mailhog . Any email sent out
will be instantly visible there.

## License

This project is licensed under the EUPL-1.2-or-later. See [LICENSE](./LICENSE) for details.
