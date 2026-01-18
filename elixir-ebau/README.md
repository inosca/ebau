# Ebau

## Developing

There are two ways to work on the elixir application:

### a) using a local installation of elixir (highly recommended)

In this case you have to install a suitable version of erlang and elixir. Ideally you use similar version
to the ones specified in the Dockerfile in the `elixir-ebau` folder.


#### Starting the dev server
You can then start the development server with:

```ex
mix phx.server
```

You can now access the application under [http://localhost:4000](http://localhost:4000). As an example the dev dashboard lives under:
[http://localhost:4000/dev/dashboard](http://localhost:4000/dev/dashboard).

### b) using the container

- Hot code reloading and browser refresh still works
- Formatting has to be done inside the container using `mix format`
- No editor or language server integration (particularly useful when working with Ash)

The application runs under the `/elixir` path which gets rewritten by the proxy. So as an example you can
access the live dashboard at [http://ember-ebau.localhost/elixir/dev/dashboard](http://ember-ebau.localhost/elixir/dev/dashboard).

### Language server

[`Expert`](https://expert-lsp.org) is the official language server. The docs have instructions on how to setup
[different editors](https://expert-lsp.org/docs/editors/).

## REPL

Elixir also has a REPL (similar to the django shell) which can be started with `iex -S mix`. You can also start
your webserver with an active REPL:

```ex
cd elixir-ebau
iex -S mix phx.server
```

This is slightly different to Django since you are effectively starting the entire system with an active REPL.
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

## Learn more

* Official website: https://www.phoenixframework.org/
* Guides: https://hexdocs.pm/phoenix/overview.html
* Docs: https://hexdocs.pm/phoenix
* Forum: https://elixirforum.com/c/phoenix-forum
* Source: https://github.com/phoenixframework/phoenix
