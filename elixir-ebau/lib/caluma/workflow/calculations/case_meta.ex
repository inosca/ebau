defmodule Caluma.Workflow.Calculations.CaseMeta do
  @moduledoc """
  Calculation that reads a value from a Caluma case's meta JSON field.

  The `key` option accepts a plain string or a `{module, opts}` resolver
  tuple (see `Caluma.Form.QuestionIdResolver`).

  The `through` option controls the path to meta:
  - `nil` — `meta[key]` (resource IS the case)
  - any atom — `<rel>.meta[key]` (resource HAS a case relationship)
  """

  use Ash.Resource.Calculation

  import Ash.Expr

  @impl true
  def init(opts) do
    case opts[:key] do
      key when is_binary(key) -> {:ok, opts}
      {mod, _opts} when is_atom(mod) -> {:ok, opts}
      _ -> {:error, "key must be a string or {module, opts} tuple"}
    end
  end

  @impl true
  def expression(opts, _context) do
    key = resolve_key(opts[:key])
    meta_expr(opts[:through], key)
  end

  defp meta_expr(nil, key), do: expr(meta[^key])

  defp meta_expr(through, key) do
    meta_ref = %Ash.Query.Ref{relationship_path: [through], attribute: :meta}

    %Ash.Query.Function.GetPath{arguments: [meta_ref, [key]]}
  end

  defp resolve_key(key) when is_binary(key), do: key
  defp resolve_key({mod, opts}), do: mod.resolve(opts)
end
