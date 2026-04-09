defmodule Ebau.Instances.GisLink do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.Instances,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer,
    extensions: [AshJsonApi.Resource]

  policies do
    policy action_type(:read) do
      authorize_if relates_to_actor_via(:service, field: :service)
    end

    policy action_type(:destroy) do
      forbid_unless actor_attribute_equals(:role, "municipality-admin")
      authorize_if relates_to_actor_via(:service, field: :service)
    end

    policy action_type(:create) do
      authorize_if actor_attribute_equals(:role, "municipality-admin")
    end
  end

  attributes do
    uuid_primary_key :id

    attribute :name, :string do
      allow_nil? false
      public? true
    end

    attribute :placeholder, :string do
      allow_nil? false
      public? true
    end
  end

  relationships do
    belongs_to :service, Ebau.User.Service do
      allow_nil? false
      attribute_type :integer
    end
  end

  actions do
    defaults [:read]

    read :read_gis_links do
      pagination offset?: true, countable: true, required?: true
    end

    read :list_gis_links_for_instance do
      argument :instance_id, :integer, allow_nil?: false
      prepare build(load: [gis_link_for_instance: %{instance_id: arg(:instance_id)}])
    end

    create :create_gis_link do
      # Needed since ember always passes relationship
      argument :service, :map
      accept [:name, :placeholder]
      change relate_actor(:service, field: :service)
    end

    destroy :destroy_gis_link
  end

  postgres do
    table "gis_links"
    repo Ebau.Repo
  end

  calculations do
    calculate :gis_link_for_instance, :string, Ebau.Instances.Calculations.GisLinkForInstance do
      argument :instance_id, :integer, allow_nil?: false
    end
  end

  json_api do
    type "gis-links"
  end
end
