defmodule Ebau.MasterData.Calculations.MappedDocumentAnswer do
  @moduledoc """
  Calculation that looks up an answer on the instance's case document and maps it to given value.

  Same as `Ebau.MasterData.Calculations.DocumentAnswer` but allows mapping of question values.
  """

  use Ash.Resource.Calculation

  @impl true
  defdelegate init(opts), to: Ebau.MasterData.Calculations.DocumentAnswer

  @impl true
  def expression(opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)
    mapping = Ebau.Caluma.Helpers.get_answer_mapping(opts[:mapping], context)

    answer_expr =
      case question_ids do
        [single_id] ->
          expr(
            first(case.document.answers,
              field: :value,
              filter: expr(question_id == ^single_id)
            )
          )

        ids ->
          expr(first(case.document.answers, field: :value, filter: expr(question_id in ^ids)))
      end

    Enum.reduce(mapping, expr(nil), fn {answer_value, mapped_value}, acc ->
      expr(
        if ^answer_expr == ^answer_value do
          ^mapped_value
        else
          ^acc
        end
      )
    end)
  end
end
