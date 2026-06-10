defmodule Caluma.Form.Calculations.DocumentAnswer do
  @moduledoc """
  Ash calculation that extracts an answer value via a filtered `has_one`
  relationship to `Caluma.Form.Answer`.

  Used by both `Caluma.Form.Extensions.Document` (for resources that *are*
  documents) and `Caluma.Workflow.Extensions.Case` (for resources that *relate*
  to a case with a document).

  The `relationship` option names the auto-generated has_one (e.g.
  `:_proposal_answer`) added by the transformer. The has_one is filtered by
  `question_id`, so this calculation just dereferences the answer's typed
  value calculation (`value_string`/`value_integer`/...).

  This is preferred over a `first/2` aggregate because AshPostgres compiles
  aggregates as `LATERAL array_agg + GROUP BY` per parent row, which is far
  slower than a plain JOIN even with a covering index.
  """

  use Ash.Resource.Calculation

  import Ash.Expr

  @impl true
  def init(opts) do
    case opts[:relationship] do
      rel when is_atom(rel) and not is_nil(rel) -> {:ok, opts}
      _ -> {:error, "relationship option is required (atom)"}
    end
  end

  @impl true
  def expression(opts, context) do
    answer_expr(opts[:relationship], field_for_type(Map.get(context, :type)))
  end

  @doc """
  Returns the typed value calculation name on `Caluma.Form.Answer` matching
  the parent calc's Ash type.
  """
  def field_for_type(Ash.Type.Integer), do: :value_integer
  def field_for_type(Ash.Type.Float), do: :value_float
  def field_for_type(Ash.Type.Boolean), do: :value_boolean
  def field_for_type(_), do: :value_string

  @doc """
  Builds the Ash expression that dereferences a typed value from the given
  filtered `has_one` relationship. Reused by mapped/mapped-list calcs.
  """
  def answer_expr(relationship, field \\ :value_string) when is_atom(relationship) do
    ref = %Ash.Query.Ref{relationship_path: [relationship], attribute: field}
    expr(^ref)
  end

  @doc """
  Like `init/1` but also validates that a `mapping` option is present and is
  either a plain map or a `{module, opts}` resolver tuple. Used by the mapped
  answer calculations.
  """
  def init_with_mapping(opts) do
    with {:ok, opts} <- init(opts),
         :ok <- validate_mapping(opts[:mapping]) do
      {:ok, opts}
    end
  end

  defp validate_mapping(m) when is_map(m), do: :ok
  defp validate_mapping({mod, _}) when is_atom(mod), do: :ok
  defp validate_mapping(_), do: {:error, "mapping must be a map or {module, opts} tuple"}

  def resolve_mapping(mapping, _context) when is_map(mapping), do: mapping
  def resolve_mapping({mod, opts}, context), do: mod.resolve(opts, context)
end
