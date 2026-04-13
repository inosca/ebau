defmodule Ebau.User.Group do
  @moduledoc """
  A CAMAC group from the legacy `GROUP` table.

  Groups link users to a role and a service. The active group for a request
  is determined by the `x-camac-group` header and becomes `actor.group`.

  Readable only by members (users who belong to the group via `UserGroup`).
  Write actions are forbidden and only used in tests with `authorize?: false`.
  """

  use Ash.Resource,
    domain: Ebau.User,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "GROUP"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type(:read) do
      authorize_if relates_to_actor_via(:users, field: :user)
    end

    policy action_type([:create, :update, :destroy]) do
      # Write actions are only used in tests with authorize?: false
      forbid_if always()
    end
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]

    read :get_group_for_actor

    create :create_group do
      argument :users, {:array, :map}
      argument :role, :map
      accept :*
      change manage_relationship(:users, type: :append)
      change manage_relationship(:role, type: :append, use_identities: [:unique_slug])
    end
  end

  attributes do
    integer_primary_key :id do
      source :GROUP_ID
    end

    attribute :name, :string do
      constraints max_length: 100
      source :NAME
    end

    attribute :service_id, :integer do
      allow_nil? true
      source :SERVICE_ID
    end

    attribute :role_id, :integer do
      allow_nil? true
      source :ROLE_ID
    end
  end

  relationships do
    belongs_to :service, Ebau.User.Service do
      define_attribute? false
    end

    belongs_to :role, Ebau.User.Role do
      define_attribute? false
    end

    many_to_many :users, Ebau.User.User do
      through Ebau.User.UserGroup
    end

    has_many :user_groups, Ebau.User.UserGroup
  end
end
