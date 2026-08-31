defmodule Caluma.Workflow.Changes.StartCase do
  @moduledoc """
  Adds a document to the `:case` argument, so the created case has one to
  write answers to. Put it before `manage_relationship(:case, ...)`:

      change {Caluma.Workflow.Changes.StartCase, form: "baugesuch"}

  `form` is a slug or a `{resolver, opts}` tuple. Does nothing when the
  caller already passes a document in `:case`.
  """

  use Ash.Resource.Change

  alias Caluma.Form.QuestionId

  @impl true
  def change(changeset, opts, _context) do
    with {:ok, %{} = input} <- Ash.Changeset.fetch_argument(changeset, :case),
         false <- Map.has_key?(input, :document) do
      slug = QuestionId.slug(Keyword.fetch!(opts, :form))

      Ash.Changeset.set_argument(
        changeset,
        :case,
        Map.put(input, :document, %{form: %{slug: slug}})
      )
    else
      _ -> changeset
    end
  end
end
