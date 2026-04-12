defmodule Ebau.User.Role do
  @moduledoc """
  A CAMAC role from the legacy `ROLE` table.

  Roles define what a user can do (e.g. `municipality-lead`,
  `municipality-admin`). Each group belongs to exactly one role.
  The role slug is stored on the `Ebau.Actor` struct as a plain string.

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
    table "ROLE"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, :destroy, update: :*, create: :*]
  end

  attributes do
    integer_primary_key :id, source: :ROLE_ID

    attribute :name, :string do
      constraints max_length: 100
      source :NAME
    end

    attribute :slug, :string do
      public? true
    end

    attribute :group_prefix, :string do
      constraints max_length: 100
      source :GROUP_PREFIX
    end

    attribute :role_parent_id, :integer do
      source :ROLE_PARENT_ID
    end
  end

  relationships do
    belongs_to :role_parent, __MODULE__, source_attribute: :role_parent_id
    has_many :groups, Ebau.User.Group
  end

  identities do
    identity :unique_slug, [:slug]
  end
end
