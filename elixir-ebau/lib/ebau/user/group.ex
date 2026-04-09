defmodule Ebau.User.Group do
  use Ash.Resource,
    domain: Ebau.User,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  alias Ebau.User.UserGroup

  postgres do
    table "GROUP"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action(:read) do
      # TODO
      authorize_if never()
    end

    policy action(:get_group_for_actor) do
      authorize_if relates_to_actor_via([:users])
    end
  end

  actions do
    defaults [:read]

    read :get_group_for_actor
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
  end

  relationships do
    belongs_to :service, Ebau.User.Service do
      define_attribute? false
    end

    many_to_many :users, Ebau.User.User do
      through Ebau.User.UserGroup
    end

    has_many :user_groups, Ebau.User.UserGroup
  end
end
