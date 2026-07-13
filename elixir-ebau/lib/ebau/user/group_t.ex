defmodule Ebau.User.GroupT do
  @moduledoc """
  Legacy `GROUP_T` translations for `Ebau.User.Group`.

  Read-only reference data. Reads are always allowed; writes are
  forbidden and only used in tests with `authorize?: false`.
  """

  use Ash.Resource,
    domain: Ebau.User,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "GROUP_T"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type(:read) do
      authorize_if always()
    end

    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end
  end

  actions do
    defaults [:read]
  end

  attributes do
    integer_primary_key :id

    attribute :group_id, :integer do
      allow_nil? false
      source :GROUP_ID
    end

    attribute :language, :string do
      allow_nil? false
      source :LANGUAGE
      constraints max_length: 2
    end

    attribute :name, :string do
      allow_nil? true
      source :NAME
      constraints max_length: 200
    end

    attribute :city, :string do
      allow_nil? true
      source :CITY
      constraints max_length: 100
    end
  end

  relationships do
    belongs_to :group, Ebau.User.Group
  end
end
