defmodule Ebau.MasterData.Calculations.DocumentAnswer do
  @moduledoc """
  Calculation that looks up an answer on the instance's case document.

  Same as `Ebau.Caluma.Calculations.DocumentAnswer` but traverses
  `case.document.answers` instead of `answers`, since this runs on Instance.
  """

  use Ash.Resource.Calculation

  @impl true
  defdelegate init(opts), to: Ebau.Caluma.Calculations.DocumentAnswer

  @impl true
  def expression(opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)

    expr(first(case.document.answers, field: :value, filter: expr(question_id in ^question_ids)))
  end
end
