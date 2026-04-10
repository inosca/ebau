defmodule Caluma.Form.Changes.CreateRowDocument do
  use Ash.Resource.Change

  @impl true
  def change(changeset, _opts, context) do
    %{slug: slug} = Ash.Changeset.get_argument(changeset, :question)
    %{id: parent_id} = Ash.Changeset.get_argument(changeset, :document)

    question = Caluma.Form.get_question_by_slug!(slug, actor: context.actor)

    next_sort =
      case Caluma.Form.get_answer_by_document_and_question(parent_id, slug,
             load: [:max_sort, question: [:row_form_id, :slug]],
             actor: context.actor
           ) do
        {:ok, answer} ->
          answer.max_sort + 1

        _ ->
          1
      end

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
  end
end
