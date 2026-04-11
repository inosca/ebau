defmodule Caluma.Form.Changes.SetFormQuestionNaturalKey do
  use Ash.Resource.Change

  alias Ash.Changeset

  @impl true
  def change(changeset, _opts, _context) do
    form_id = Changeset.get_attribute(changeset, :form_id)
    question_id = Changeset.get_attribute(changeset, :question_id)

    Changeset.force_change_attribute(changeset, :id, "#{form_id}.#{question_id}")
  end
end
