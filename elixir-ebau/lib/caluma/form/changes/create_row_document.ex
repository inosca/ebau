defmodule Caluma.Form.Changes.CreateRowDocument do
  @moduledoc """
  Ash change that wires up a new row document for a table question.

  Sets the form from the question's `row_form_id`, links the document to the
  parent answer via `AnswerDocument`, and inserts it at sort position 0
  (shifting existing rows up).
  """

  use Ash.Resource.Change

  @impl true
  def change(changeset, _opts, context) do
    %{slug: slug} = Ash.Changeset.get_argument(changeset, :question)
    %{id: parent_id} = Ash.Changeset.get_argument(changeset, :document)
    action_opts = Ash.Context.to_opts(context)

    question =
      case Caluma.Form.get_answer_by_document_and_question(
             parent_id,
             slug,
             Keyword.put(action_opts, :load, question: [:row_form_id, :slug])
           ) do
        {:ok, answer} ->
          answer.question

        {:error, %Ash.Error.Invalid{errors: [%Ash.Error.Query.NotFound{} | _]}} ->
          Caluma.Form.get_question_by_slug!(slug, action_opts)
      end

    if question.type == :table do
      changeset
      |> Ash.Changeset.force_change_attribute(:family_id, parent_id)
      |> Ash.Changeset.manage_relationship(:form, %{slug: question.row_form_id}, type: :append)
      |> Ash.Changeset.before_action(fn cs ->
        Caluma.Form.AnswerDocument
        |> Ash.Query.for_read(
          :get_by_document_and_question,
          %{document_id: parent_id, question_id: question.slug},
          actor: context.actor
        )
        |> Ash.bulk_update!(:shift_sort_up, %{}, actor: context.actor, authorize?: false)

        cs
      end)
      |> Ash.Changeset.manage_relationship(
        :parent_answers,
        [%{document_id: parent_id, question_id: question.slug, sort: 0}],
        on_lookup: :relate,
        on_no_match: :create,
        join_keys: [:sort],
        use_identities: [:document_question]
      )
    else
      Ash.Changeset.add_error(changeset, "question #{slug} is not a table question")
    end
  end
end
