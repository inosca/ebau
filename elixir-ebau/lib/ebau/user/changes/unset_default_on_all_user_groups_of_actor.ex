defmodule Ebau.User.Changes.UnsetDefaultOnAllUserGroupsOfActor do
  @moduledoc """
  Before action change that clears `default_group` on every `UserGroup`
  belonging to the acting user, so only one row can carry the flag after
  the outer `set_default_user_group` action sets it on the target row.

  Runs as a single bulk update keyed by `user_id` instead of iterating.
  """

  use Ash.Resource.Change

  @impl true
  def change(changeset, _opts, context) do
    Ash.Changeset.before_action(changeset, fn changeset ->
      Ebau.User.UserGroup
      |> Ash.Query.for_read(:read_for_actor, %{}, actor: context.actor)
      |> Ebau.User.clear_default_user_group!(actor: context.actor)

      changeset
    end)
  end
end
