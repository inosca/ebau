defmodule Ebau.Caluma.Calculations.DocumentAnswer do
  @moduledoc """
  Calculation that looks up an answer on a document by question ID,
  with per-canton question ID mapping.

  Expects a `question_ids` option — a map from canton atom to Caluma
  question ID string. Must include at least a `:default` key.

  ## Example

      calculate :plot_number,
                Caluma.Form.Types.AnswerValue,
                {Ebau.Caluma.Calculations.DocumentAnswer,
                 question_ids: %{default: "parzellennummer", gr: "parzellennummer"}}

  The canton is read from `context.actor.canton` at query time. If the
  canton has no specific mapping, the `:default` entry is used.
  """

  use Ash.Resource.Calculation

  @impl true
  def init(opts) do
    question_ids = opts[:question_ids]

    cond do
      !is_map(question_ids) ->
        {:error, "question_ids option must be a map"}

      !Map.has_key?(question_ids, :default) ->
        {:error, "question_ids must include a :default key"}

      true ->
        {:ok, opts}
    end
  end

  @impl true
  def expression(opts, context) do
    question_id =
      if context.actor && context.actor.canton do
        opts[:question_ids][context.actor.canton] || opts[:question_ids][:default]
      else
        opts[:question_ids][:default]
      end

    expr(first(answers, field: :value, filter: expr(question_id == ^question_id)))
  end
end
