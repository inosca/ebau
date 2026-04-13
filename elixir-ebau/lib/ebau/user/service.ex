defmodule Ebau.User.Service do
  @moduledoc """
  A CAMAC service (Dienststelle) from the legacy `SERVICE` table.

  Services represent organizational units like municipalities or cantonal
  offices. Each service belongs to a `ServiceGroup` and owns `GisLink`
  templates. The actor's service is resolved from `actor.group.service_id`.

  Reads require an authenticated actor. Writes are forbidden and only
  used in tests with `authorize?: false`.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.User,
    data_layer: AshPostgres.DataLayer,
    extensions: [AshJsonApi.Resource],
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "SERVICE"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type(:read) do
      authorize_if actor_present()
    end

    policy action_type(:create) do
      # Write actions are only used in tests with authorize?: false
      forbid_if always()
    end
  end

  actions do
    defaults [:read]

    create :create_service do
      argument :groups, {:array, :map}
      argument :service_group, :map
      accept :*
      change manage_relationship(:groups, :groups, type: :append)
      change manage_relationship(:service_group, :service_group, type: :direct_control)
    end
  end

  attributes do
    integer_primary_key :id do
      source :SERVICE_ID
    end

    attribute :name, :string do
      constraints max_length: 100
      source :NAME
      public? true
    end

    attribute :sort, :integer do
      default 0
      allow_nil? false
      source :SORT
    end

    attribute :service_group_id, :integer do
      allow_nil? false
      source :SERVICE_GROUP_ID
      public? true
    end
  end

  relationships do
    has_many :gis_links, Ebau.Instances.GisLink, domain: Ebau.Instances
    has_many :groups, Ebau.User.Group

    belongs_to :service_group, Ebau.User.ServiceGroup,
      allow_nil?: false,
      define_attribute?: false
  end

  json_api do
    type "services"
  end
end
