defmodule Caluma.Form.Changes.CreateRowDocument do
  @moduledoc """
  Ash change that wires up a new row document for a table question.

  Sets the form from the question's `row_form_id`, links the document to the
  parent answer via `AnswerDocument`, and computes the next sort order.
  """

  use Ash.Resource.Change

  @impl true
  def change(changeset, _opts, context) do
    %{slug: slug} = Ash.Changeset.get_argument(changeset, :question)
    %{id: parent_id} = Ash.Changeset.get_argument(changeset, :document)
    action_opts = Ash.Context.to_opts(context)

    {question, next_sort} =
      case Caluma.Form.get_answer_by_document_and_question(
             parent_id,
             slug,
             Keyword.put(action_opts, :load, [:max_sort, question: [:row_form_id, :slug]])
           ) do
        {:ok, answer} ->
          {answer.question, (answer.max_sort || 0) + 1}

        {:error, %Ash.Error.Invalid{errors: [%Ash.Error.Query.NotFound{} | _]}} ->
          {Caluma.Form.get_question_by_slug!(slug, action_opts), 1}
      end

    if question.type == :table do
      changeset
      |> Ash.Changeset.force_change_attribute(:family_id, parent_id)
      |> Ash.Changeset.manage_relationship(:form, %{slug: question.row_form_id}, type: :append)
      |> Ash.Changeset.manage_relationship(
        :parent_answers,
        [%{document_id: parent_id, question_id: question.slug, sort: next_sort}],
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
