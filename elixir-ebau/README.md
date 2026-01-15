# Ebau

## Developing

There are two ways to work on the elixir application:

### a) using a local installation of elixir (highly recommended)

In this case you have to install a suitable version of erlang and elixir. Ideally you use similar version
to the ones specified in the Dockerfile in the `elixir-ebau` folder.

### b) using the container

- Hot code reloading and browser refresh still works
- Formatting has to be done inside the container using `mix format`
- No editor or language server integration (particularly useful when working with Ash)

### Language server

[`Expert`](https://expert-lsp.org) is the official language server. The docs have instructions on how to setup
[different editors](https://expert-lsp.org/docs/editors/).


To start your Phoenix server:

* Run `mix setup` to install and setup dependencies
* Start Phoenix endpoint with `mix phx.server` or inside IEx with `iex -S mix phx.server`

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](https://hexdocs.pm/phoenix/deployment.html).

## Learn more

* Official website: https://www.phoenixframework.org/
* Guides: https://hexdocs.pm/phoenix/overview.html
* Docs: https://hexdocs.pm/phoenix
* Forum: https://elixirforum.com/c/phoenix-forum
* Source: https://github.com/phoenixframework/phoenix
