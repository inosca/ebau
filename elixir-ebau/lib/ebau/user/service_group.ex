defmodule Ebau.User.ServiceGroup do
  @moduledoc """
  A grouping of services from the legacy `SERVICE_GROUP` table.

  Service groups categorize services by type (e.g. municipalities,
  cantonal offices). Identified by a unique slug.

  Read-only reference data. Reads are always allowed; writes are
  forbidden and only used in tests with `authorize?: false`.
  """

  use Ash.Resource,
    data_layer: AshPostgres.DataLayer,
    domain: Ebau.User,
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
    repo Ebau.Repo
    table "SERVICE_GROUP"
    migrate? false
  end

  actions do
    defaults [:read, :destroy, update: :*, create: :*]
  end

  attributes do
    integer_primary_key :id do
      source :SERVICE_GROUP_ID
    end

    attribute :name, :string do
      source :NAME
    end

    attribute :sort, :integer, allow_nil?: true

    attribute :slug, :string do
      public? true
    end
  end

  identities do
    identity :unique_slug, [:slug]
  end
end
