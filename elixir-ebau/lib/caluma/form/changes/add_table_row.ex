defmodule Caluma.Form.Changes.AddTableRow do
  @moduledoc """
  Makes the document being created a row of a table question: its family is
  the parent document, its form the question's row form, and it is linked to
  the parent's answer to the question (created if missing) at `sort: 0`.

  ## Options

  * `document_argument` (required) — the `:uuid` argument holding the parent
    document id.
  * `question` — `{resource, table_name}`, where `resource` declares
    `table table_name` in a `caluma_document` block.
  * `question_argument` — the `:string` argument holding the question slug,
    for when the question is only known at call time.

  ```
  # MyApp.Building — a Document or Case resource
  caluma_document do
    table :plots, MyApp.Plot, question_id: "parzellen"
  end

  # MyApp.Plot
  create :create do
    argument :document_id, :uuid, allow_nil?: false
    argument :plot_number, :string

    change {Caluma.Form.Changes.AddTableRow,
            question: {MyApp.Building, :plots}, document_argument: :document_id}

    change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:plot_number]}
  end
  ```
  """

  use Ash.Resource.Change

  alias Caluma.Form.Extensions.Document.Info

  @impl true
  def change(changeset, opts, context) do
    parent_id = Ash.Changeset.get_argument(changeset, opts[:document_argument])
    slug = question_slug(changeset, opts)
    question = Caluma.Form.get_question_by_slug!(slug, scope: context)

    changeset
    |> Ash.Changeset.manage_relationship(:family, parent_id, type: :append)
    |> Ash.Changeset.force_change_attribute(:form_id, question.row_form_id)
    |> Ash.Changeset.manage_relationship(
      :parent_answers,
      [%{document_id: parent_id, question_id: slug}],
      on_lookup: {:relate, :prepend},
      on_no_match: {:create, :create, :prepend},
      use_identities: [:document_question]
    )
  end

  defp question_slug(changeset, opts) do
    case opts[:question] do
      {resource, name} -> Info.question_slug!(resource, name)
      nil -> Ash.Changeset.get_argument(changeset, opts[:question_argument])
    end
  end
end
