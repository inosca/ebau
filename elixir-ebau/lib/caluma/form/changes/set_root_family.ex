defmodule Caluma.Form.Changes.SetRootFamily do
  @moduledoc """
  Pre-generates the new document's primary key and points its `family_id` at
  itself, mirroring upstream Caluma's `post_init` signal in
  `caluma/caluma_form/signals.py`.

  Without this, root documents inherit the postgres `gen_random_uuid()`
  default for `family_id`, producing a dangling reference. By forcing
  `family_id == id` for root documents we keep the invariant that every
  document — root or row — links back to its family root via `family`.
  """

  use Ash.Resource.Change

  alias Ash.Changeset

  @impl true
  def change(changeset, _opts, _context) do
    id = Changeset.get_attribute(changeset, :id) || Ash.UUID.generate()

    changeset
    |> Changeset.force_change_attribute(:id, id)
    |> Changeset.force_change_attribute(:family_id, id)
  end
end
