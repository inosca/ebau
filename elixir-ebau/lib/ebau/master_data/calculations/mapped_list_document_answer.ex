defmodule Ebau.MasterData.Calculations.MappedListDocumentAnswer do
  @moduledoc """
  SQL-backed calculation that reads a list-valued Caluma answer and maps each element.

  Use `mapped_list_answer` in the `master_data` DSL for multi-select questions.
  Falls back to `calculate/3` when evaluating already-loaded records in memory.
  """

  use Ash.Resource.Calculation

  @impl true
  defdelegate init(opts), to: Ebau.MasterData.Calculations.DocumentAnswer

  @impl true
  def load(_query, _opts, _context), do: [case: [document: :answers]]

  @impl true
  def expression(opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)
    mapping = Ebau.Caluma.Helpers.get_answer_mapping(opts[:mapping], context)
    answer_expr = answer_expr(question_ids)

    case array_item_type(context.type) do
      Ash.Type.Boolean ->
        boolean_array_expr(answer_expr, mapping)

      Ash.Type.Integer ->
        integer_array_expr(answer_expr, mapping)

      Ash.Type.Float ->
        float_array_expr(answer_expr, mapping)

      _ ->
        string_array_expr(answer_expr, mapping)
    end
  end

  @impl true
  def calculate(records, opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)
    mapping = Ebau.Caluma.Helpers.get_answer_mapping(opts[:mapping], context)

    Enum.map(records, fn record ->
      answer =
        Enum.find(record.case.document.answers, fn a -> a.question_id in question_ids end)

      case answer do
        nil -> nil
        %{value: value} when is_list(value) -> Enum.map(value, &Map.get(mapping, &1))
        %{value: value} -> [Map.get(mapping, value)]
      end
    end)
  end

  defp answer_expr(question_ids) do
    expr(first(case.document.answers, field: :value, filter: expr(question_id in ^question_ids)))
  end

  defp array_item_type({:array, type}), do: type
  defp array_item_type(type), do: type

  defp string_array_expr(answer_expr, mapping) do
    expr(
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

  defp boolean_array_expr(answer_expr, mapping) do
    expr(
      if is_nil(^answer_expr) do
        nil
      else
        fragment(
          """
          (
            SELECT COALESCE(
              array_agg(
                CASE (?::jsonb ->> elem.value)
                  WHEN 'true' THEN true
                  WHEN 'false' THEN false
                  ELSE NULL
                END
                ORDER BY elem.ord
              ),
              ARRAY[]::boolean[]
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

  defp integer_array_expr(answer_expr, mapping) do
    expr(
      if is_nil(^answer_expr) do
        nil
      else
        fragment(
          """
          (
            SELECT COALESCE(
              array_agg(((?::jsonb ->> elem.value))::integer ORDER BY elem.ord),
              ARRAY[]::integer[]
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

  defp float_array_expr(answer_expr, mapping) do
    expr(
      if is_nil(^answer_expr) do
        nil
      else
        fragment(
          """
          (
            SELECT COALESCE(
              array_agg(((?::jsonb ->> elem.value))::double precision ORDER BY elem.ord),
              ARRAY[]::double precision[]
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
