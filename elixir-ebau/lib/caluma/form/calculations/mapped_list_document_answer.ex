defmodule Caluma.Form.Calculations.MappedListDocumentAnswer do
  @moduledoc """
  SQL-backed calculation that reads a list-valued Caluma answer and maps
  each element.

  The transformer passes a `relationship` option naming a filtered
  `has_one` relationship to `Caluma.Form.Answer` (one per declared answer).

  The `mapping` option accepts either a flat `%{string => value}` map or
  a `{resolver_module, opts}` tuple (see `Caluma.Form.QuestionIdResolver`).

  Falls back to `calculate/3` when evaluating already-loaded records in memory.
  """

  use Ash.Resource.Calculation

  import Ash.Expr

  alias Caluma.Form.Calculations.DocumentAnswer

  @impl true
  def init(opts) do
    with {:ok, opts} <- DocumentAnswer.init(opts) do
      case opts[:mapping] do
        m when is_map(m) -> {:ok, opts}
        {mod, _} when is_atom(mod) -> {:ok, opts}
        _ -> {:error, "mapping must be a map or {module, opts} tuple"}
      end
    end
  end

  @impl true
  def load(_query, opts, _context) do
    [{opts[:relationship], :value}]
  end

  @impl true
  def expression(opts, context) do
    mapping = DocumentAnswer.resolve_mapping(opts[:mapping], context)
    answer_expr = DocumentAnswer.answer_expr(opts[:relationship], :value)

    case array_item_type(context.type) do
      # There were already implementations for more types which can be seen in commit
      # ad19702 but since caluma only supports string list answers lets not bloat the code.
      Ash.Type.String -> string_array_expr(answer_expr, mapping)
      _ -> {:error, "mapping only supports strings"}
    end
  end

  @impl true
  def calculate(records, opts, context) do
    rel = opts[:relationship]
    mapping = DocumentAnswer.resolve_mapping(opts[:mapping], context)

    Enum.map(records, fn record ->
      case Map.get(record, rel) do
        nil -> nil
        %Ash.NotLoaded{} -> nil
        %{value: value} when is_list(value) -> Enum.map(value, &Map.get(mapping, &1))
        %{value: value} -> [Map.get(mapping, value)]
      end
    end)
  end

  defp array_item_type({:array, type}), do: type
  defp array_item_type(type), do: type

  defp string_array_expr(answer_expr, mapping) do
    expr(
      # NOTE: Do NOT use `if !is_nil(...)` here — Ash expressions don't
      # support the `!` operator. Use `is_nil` with nil/else instead.
      if is_nil(^answer_expr) do
        nil
      else
        fragment(
          """
          (
            SELECT COALESCE(
              array_agg((?::jsonb ->> elem.value) ORDER BY elem.ord),
              ARRAY[]::text[]
            )
            FROM jsonb_array_elements_text(
              CASE jsonb_typeof(?::jsonb)
                WHEN 'array' THEN ?::jsonb
                ELSE jsonb_build_array(?::jsonb)
              END
            ) WITH ORDINALITY AS elem(value, ord)
          )
          """,
          ^mapping,
          ^answer_expr,
          ^answer_expr,
          ^answer_expr
        )
      end
    )
  end
end
