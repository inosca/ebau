defmodule Ebau.User.UserGroup do
  @moduledoc """
  Join table between users and groups from the legacy `USER_GROUP` table.

  Read-only reference data. Reads are always allowed; writes are
  forbidden and only used in tests with `authorize?: false`.
  """

  use Ash.Resource,
    domain: Ebau.User,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  policies do
    policy action_type(:read) do
      authorize_if always()
    end

    policy action_type([:create, :update, :destroy]) do
      # Write actions are only used in tests with authorize?: false
      forbid_if always()
    end
  end

  postgres do
    table "USER_GROUP"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]
  end

  attributes do
    integer_primary_key :id do
      source :ID
    end

    attribute :default_group, :integer do
      default 0
      source :DEFAULT_GROUP
    end

    attribute :user_id, :integer, allow_nil?: false, source: :USER_ID
    attribute :group_id, :integer, allow_nil?: false, source: :GROUP_ID
  end

  relationships do
    belongs_to :user, Ebau.User.User
    belongs_to :group, Ebau.User.Group
  end
end
