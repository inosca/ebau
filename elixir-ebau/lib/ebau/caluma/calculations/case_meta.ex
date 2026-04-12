defmodule Ebau.Caluma.Calculations.CaseMeta do
  @moduledoc """
  Calculation that reads a value from the case's meta JSON field,
  with per-canton key mapping.

  Expects a `keys` option, a map from canton atom to meta key string.
  Must include at least a `:default` key.

  ## Example

      calculate :dossier_number,
                :string,
                {Ebau.Caluma.Calculations.CaseMeta,
                 keys: %{default: "dossier-number"}}

  The canton is read from `context.canton` at query time. If the
  canton has no specific mapping, the `:default` entry is used.
  """

  use Ash.Resource.Calculation

  @impl true
  def init(opts) do
    keys = opts[:keys]

    cond do
      !is_map(keys) ->
        {:error, "keys option must be a map"}

      !Map.has_key?(keys, :default) ->
        {:error, "keys must include a :default key"}

      true ->
        {:ok, opts}
    end
  end

  @impl true
  def expression(opts, context) do
    key = Ebau.Caluma.Helpers.get_canton_value(opts[:keys], context)

    expr(case.meta[^key])
  end
end
