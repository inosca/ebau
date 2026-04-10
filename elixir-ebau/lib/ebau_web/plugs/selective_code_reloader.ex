defmodule EbauWeb.Plugs.SelectiveCodeReloader do
  @moduledoc """
  Wraps `Phoenix.CodeReloader` to only invoke `mix compile` when source
  files have actually changed, avoiding the ~1s noop overhead on every
  request.

  Checks whether any `.ex`, `.heex`, or `.po` file in `lib/` or
  `priv/gettext/` is newer than the Elixir compiler manifest. If nothing
  is stale the plug is a no-op (microseconds). If something changed it
  delegates to `Phoenix.CodeReloader` as normal.

  Only used in dev/test (guarded by `code_reloading?` in the endpoint).
  """

  @behaviour Plug

  def init(opts), do: Phoenix.CodeReloader.init(opts)

  def call(conn, opts) do
    if stale?() do
      Phoenix.CodeReloader.call(conn, opts)
    else
      conn
    end
  end

  defp stale? do
    sources =
      Path.wildcard("lib/**/*.ex") ++
        Path.wildcard("lib/**/*.heex") ++
        Path.wildcard("priv/gettext/**/*.po")

    manifests = Mix.Tasks.Compile.Elixir.manifests()

    Mix.Utils.stale?(sources, manifests)
  end
end
