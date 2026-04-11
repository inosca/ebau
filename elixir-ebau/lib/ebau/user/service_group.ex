defmodule Ebau.User.ServiceGroup do
  use Ash.Resource,
    data_layer: AshPostgres.DataLayer,
    domain: Ebau.User

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
