# Ebau

## Developing

There are two ways to work on the elixir application:

### Development and setups
#### a) using a local installation of elixir (highly recommended)

In this case you have to install a suitable version of erlang and elixir. Ideally you use similar version
to the ones specified in the Dockerfile in the `elixir-ebau` folder.


##### Starting the dev server
You can then start the development server with:

```ex
mix phx.server
```

You can now access the application under [http://localhost:4000](http://localhost:4000). As an example the dev dashboard lives under:
[http://localhost:4000/dev/dashboard](http://localhost:4000/dev/dashboard).

#### b) using the container

- Hot code reloading and browser refresh still works
- Formatting has to be done inside the container using `mix format`
- No editor or language server integration (particularly useful when working with Ash)

The application runs under the `/elixir` path which gets rewritten by the proxy. So as an example you can
access the live dashboard at [http://ember-ebau.localhost/elixir/dev/dashboard](http://ember-ebau.localhost/elixir/dev/dashboard).

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

```ex
cd elixir-ebau
iex -S mix phx.server
```

This is slightly different to most(?) languages that might be used to since you are effectively starting the entire **system** with an active REPL.
As an example you can then open a LiveView in the browser and inspect its process in the iex shell:

```ex
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

```text
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

## Test fixtures

Some Elixir tests load legacy JSON fixture data that originates from Django canton config.

In test environment, fixture loading uses vendored files under:

```text
priv/test_fixtures/
```

Vendored fixtures mirror all canton directories matching `kt_*`.

This avoids making CI depend on a full `../django` checkout just to run Elixir tests.

Refresh vendored fixtures with:

```bash
mix ebau.vendor_test_fixtures
```

### Explicit loading in tests

Keep fixture setup explicit in test `setup` blocks:

```elixir
setup do
  Ebau.Test.CantonFixtures.load_canton_config!(:so)
  :ok
end
```

For smaller and faster setup, load only selected files:

```elixir
setup do
  Ebau.Test.CantonFixtures.load_canton_files!(:so, [
    "user.json",
    "caluma_workflow.json",
    "caluma_form.json"
  ])

  :ok
end
```

### Overriding fixture root

Fixture root can be overridden with:

```bash
LEGACY_FIXTURE_ROOT=/path/to/fixtures mix test
```

Resolution order is:

1. `LEGACY_FIXTURE_ROOT`
2. `config :ebau, :legacy_fixture_root`
3. fallback `../django`

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
