defmodule Ebau.User.UserGroup do
  @moduledoc """
  Join table between users and groups from the legacy `USER_GROUP` table.

  Reads are allowed for any authenticated actor. The only writes permitted in real code are
  `:set_default_user_group` and `:clear_default_user_group`.
  Everything else is test-only and must use `authorize?: false` in tests.
  """

  use Ash.Resource,
    domain: Ebau.User,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  policies do
    policy action_type(:read) do
      forbid_unless actor_present()
      authorize_if always()
    end

    policy action([:set_default_user_group, :clear_default_user_group]) do
      authorize_if relates_to_actor_via(:user, field: :user)
    end
  end

  postgres do
    table "USER_GROUP"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]

    read :read_for_actor do
      description "Lists all UserGroup rows belonging to the acting user."
      filter expr(user_id == ^actor([:user, :id]))
    end

    update :set_default_user_group do
      change Ebau.User.Changes.UnsetDefaultOnAllUserGroupsOfActor
      change set_attribute(:default_group, 1)
      require_atomic? false
    end

    update :clear_default_user_group do
      change atomic_update(:default_group, 0)
    end
  end

  attributes do
    integer_primary_key :id do
      source :ID
    end

    attribute :default_group, :integer do
      default 0
      source :DEFAULT_GROUP
    end

    attribute :user_id, :integer do
      allow_nil? false
      source :USER_ID
    end

    attribute :group_id, :integer do
      allow_nil? false
      source :GROUP_ID
    end
  end

  relationships do
    belongs_to :user, Ebau.User.User
    belongs_to :group, Ebau.User.Group
  end
end
