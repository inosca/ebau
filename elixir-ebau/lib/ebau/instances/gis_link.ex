defmodule Ebau.Instances.GisLink do
  @moduledoc """
  Configurable GIS link templates scoped to a service.

  A GIS link stores a human-readable name and a placeholder URL template such as
  `https://example.com?x={x}&y={y}`. For a concrete instance, the
  `gis_link_for_instance` calculation replaces `{x}` and `{y}` with the first
  available plot coordinates from the instance's Caluma data.
  """

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
      forbid_unless Ebau.User.Policies.IsAdminRole
      authorize_if relates_to_actor_via(:service, field: :service)
    end

    policy action_type(:create) do
      authorize_if Ebau.User.Policies.IsAdminRole
    end

    policy action_type(:update) do
      forbid_if always()
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
      domain Ebau.User
      allow_nil? false
      attribute_type :integer
    end
  end

  actions do
    defaults [:read]

    read :read_gis_links do
      description "Lists GIS link templates visible to the actor's service."

      pagination do
        offset? true
        countable true
        required? true
      end

      prepare build(sort: :name)
    end

    read :list_gis_links_for_instance do
      description """
      Lists GIS link templates and preloads the resolved link for a specific instance.

      The returned records include the `gis_link_for_instance` calculation, which
      replaces `{x}` and `{y}` in the placeholder URL with the first available
      plot coordinates of the instance.
      """

      argument :instance_id, :integer do
        description "The instance whose plot coordinates should be injected into each GIS link."
        allow_nil? false
      end

      prepare build(load: [gis_link_for_instance: %{instance_id: arg(:instance_id)}])
    end

    create :create_gis_link do
      description """
      Creates a new GIS link template for the actor's service.

      The frontend still sends a `service` relationship payload, but the action
      ignores that input and always relates the created record to the actor's service.
      """

      argument :service, :map do
        description "Ignored frontend relationship payload; the actor's service is used instead."
      end

      accept [:name, :placeholder]
      change relate_actor(:service, field: :service)
    end

    destroy :destroy_gis_link do
      description "Deletes a GIS link template."
    end
  end

  postgres do
    table "gis_links"
    repo Ebau.Repo
  end

  calculations do
    calculate :gis_link_for_instance, :string, Ebau.Instances.Calculations.GisLinkForInstance do
      argument :instance_id, :integer do
        allow_nil? false
      end
    end
  end

  json_api do
    type "gis-links"
  end
end
