defmodule Ebau.Instances.GisLinks do
  use Ash.Resource, otp_app: :ebau, domain: Ebau.Instances, data_layer: AshPostgres.DataLayer, authorizers: Ash.Policy.Authorizer

  policies do
    policy action_type(:read) do
      authorize_if relates_to_actor_via([:service, :groups], field: :group)
      # authorize_if expr(service_id == ^actor(:current_group_service_id))
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
    belongs_to :service, Ebau.Users.Service do
      allow_nil? false
      attribute_type :integer
    end
  end

  actions do
    defaults [:read]

    read :list_gis_links_for_instance do
      argument :instance_id, :integer, allow_nil?: false
      prepare build(load: [gis_link_for_instance: %{instance_id: arg(:instance_id)}])
    end

    create :create_gis_link do
      # todo remove service_id here and do proper handling
      accept [:name, :placeholder, :service_id]
    end
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
end
