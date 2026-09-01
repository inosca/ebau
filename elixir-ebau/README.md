# Ebau

[Code Documentation](https://camac-ng.pages.adfinis.com/camac-ng/elixir-ebau/readme.html)

## Developing

There are two ways to work on the elixir application:

### Development and setups
#### a) using a local installation of elixir (highly recommended)

In this case you have to install a suitable version of erlang and elixir. Ideally you use similar version
to the ones specified in the Dockerfile in the `elixir-ebau` folder.


##### Starting the dev server
You can then start the development server with:

```bash
APPLICATION=kt_xy mix phx.server
```

The `APPLICATION` variable is only needed at **build time**, where it selects
the canton whose SCSS (`css/app-<canton>.scss`) gets compiled into `app.css`. At
runtime the canton is read from the dotenv file (`../.env`). To avoid passing it
manually on the host, use [`direnv`](https://direnv.net): this folder contains
an `.envrc` that loads the repo-root `.env` (the same file docker compose
reads), so the build picks up your active canton automatically. Set it up once:

```bash
# Install `direnv` (e.g. `apt install direnv`), then hook it into your shell by
# adding this to ~/.bashrc:
eval "$(direnv hook bash)"

# Reload your shell, then allow the .envrc (run once, from elixir-ebau/):
direnv allow .
```

Afterwards you can just run `mix phx.server` (if you changed canton, make sure
to run `mix clean` first, see [switching cantons](#switching-cantons)) and it
picks up the canton from `.env`.

You can now access the application under [http://localhost:4000](http://localhost:4000). As an example the dev dashboard lives under:
[http://localhost:4000/dev/dashboard](http://localhost:4000/dev/dashboard).

#### b) using the container

- Hot code reloading and browser refresh still works
- Formatting has to be done inside the container using `mix format`
- No editor or language server integration (particularly useful when working with Ash)

The application runs under the `/elixir` path which gets rewritten by the proxy. So as an example you can
access the live dashboard at [http://ember-ebau.localhost/elixir/dev/dashboard](http://ember-ebau.localhost/elixir/dev/dashboard).

### Switching cantons
To compile / test a specific canton:

```bash
mix clean
mix compile
mix test
```

Always run `mix clean` before switching canton otherwise you will get
a compile config mismatch error.

Currently supported cantons are:
- kt_so
- kt_gr
- No canton set which will default to demo

For an example look at ./Makefile test-all.

### Language server

#### Expert (official LSP)

[`Expert`](https://expert-lsp.org) is the official language server. The docs have instructions on how to setup
[different editors](https://expert-lsp.org/docs/editors/).

#### Elixir-LS

[`Elixir-LS`](https://github.com/elixir-lsp/elixir-ls) is an alternative language server that can be used. It is slightly slower but it provides very good Ash integration.
In the past there were 3 different language server projects which have all been united now under the official LSP which is `Expert`.
If you find that you are struggling with `Expert` you might want to give `Elixir-LS` a shot.

### REPL

Elixir also has a REPL (similar to the django shell) which can be started with `iex -S mix`. You can also start
your webserver with an active REPL:

```bash
cd elixir-ebau
iex -S mix phx.server
```

This is slightly different to most(?) languages that might be used to since you are effectively starting the entire **system** with an active REPL.
As an example you can then open a LiveView in the browser and inspect its process in the iex shell:

```elixir
# open a liveview in the browser, as an example http://localhost:4000/dev/dashboard and then run this in your iex
Phoenix.LiveView.Debug.list_liveviews()
# Lets mess around with this liveview process a bit:
[%{pid: pid}] = Phoenix.LiveView.Debug.list_liveviews() # we pattern match the pid
# Lets have a look what this process is:
Process.info(pid) # reductions is roughly how much work it is doing
# We can also check out how much memory it is using
Process.info(pid, :memory)
# Go back to your browser and run this command to kill the liveview
Process.exit(pid, :kill)
# You will see that there is a refresh and in your console you get the message that the liveview has reconnected
```

### `mix.exs`

The `mix.exs` file is the `package.json` or `pyproject.toml` equivalent of an Elixir project. The `aliases` function defines a bunch of aliases that you can use
to make your life slightly easier. One that you might find particularly useful is `mix precommit`.

## Docs

Generate project docs with:

```bash
mix docs
```

This writes the generated site to:

```
doc/index.html
```

The docs include:

- module docs from `@moduledoc`
- action and argument docs from Ash descriptions
- this `README.md` as the main entry page

On the default branch, GitLab CI publishes the generated docs via GitLab Pages
under the `elixir-ebau/` subpath so they can coexist with other generated docs in
the monorepo.

For merge request pipelines, GitLab CI also publishes a preview deployment under a
merge-request specific path prefix when the GitLab instance supports parallel Pages
deployments. The Elixir docs still live under the `elixir-ebau/` subpath inside
that preview.

## Dependency audit

The `audit-elixir` CI job runs `mix hex.audit`, which reports dependencies whose
authors have retired the published version (deprecated, security issue, invalid
or pulled release). The job is `allow_failure: true`, so a finding shows up as a
warning on the pipeline rather than blocking the merge request - but it should
still be dealt with.

To reproduce the warning locally, run:

```bash
mix clean
mix deps.get
mix hex.audit
```

The output lists each affected package with its locked version and the
retirement reason. Update those packages to a non-retired version:

```bash
mix deps.update <package> [<package> ...]
```

Then re-run `mix hex.audit` to confirm the warning is gone and commit the
resulting `mix.lock` change.

## Legacy config fixtures

`Ebau.Legacy.ConfigLoader` (used by `mix ebau.load_config`) reads legacy JSON
config from a Django canton checkout. Tests do not load these fixtures; they build
forms and workflows with the helpers in `test/support/` instead.

Fixture root can be overridden with:

```bash
LEGACY_FIXTURE_ROOT=/path/to/fixtures mix test
```

Resolution order is:

1. `LEGACY_FIXTURE_ROOT`
2. `config :ebau, :legacy_fixture_root`
3. fallback `../django`

## Authentication in tests

The REST API is protected by `EbauWeb.Plugs.KeycloakBearerAuth`, which resolves
a bearer token to an `Ebau.User.User` via an OAuth2 adapter. The adapter module
is injectable through config:

```elixir
config :ebau, :oauth2_module, EbauWeb.OAuth2Dummy
```

- Production/dev (default): `EbauWeb.OAuth2` hits the Keycloak userinfo
  endpoint and maps the email claim to a local user.
- Test (`config/test.exs`): `EbauWeb.OAuth2Dummy`, where the bearer token is
  simply the user id (e.g. `"1"`), looked up directly. No Keycloak server needed.

Both implement the `EbauWeb.Behaviours.OAuth2` behaviour (single `fetch_user/1`
callback).

In tests, build an authenticated conn with the helper from `EbauWeb.ConnCase`:

```elixir
conn = authenticated_rest_api_conn(conn, actor)
```

It sets `authorization: "Bearer <user.id>"` and the `x-camac-group` header.

## Cantonal theming of uikit

Cantonal theming of uikit is done using custom input files to dart_sass. The `runtime.exs` file uses the `APPLICATION`
env variable to decide which cantonal `.scss` file should be used. It then compiles it and writes to `app.css` which is
then served.

Instead of `_variables-gr.scss` that then gets rewritten to `variables.scss` during build time we instead have a `app-kt_gr.scss` which
includes shared theming stuff (mainly the base uikit things) and then gets built and served as `app.css` by sass.

If you change canton while having the dev server running you need to restart the dev server.

## Learn more

* Official website: https://www.phoenixframework.org/
* Guides: https://hexdocs.pm/phoenix/overview.html
* Docs: https://hexdocs.pm/phoenix
* Forum: https://elixirforum.com/c/phoenix-forum
* Source: https://github.com/phoenixframework/phoenix
