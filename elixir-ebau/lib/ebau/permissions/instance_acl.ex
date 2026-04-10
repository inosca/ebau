defmodule Ebau.Permissions.InstanceACL do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.Permissions,
    data_layer: AshPostgres.DataLayer,
    authorizers: [Ash.Policy.Authorizer]

  postgres do
    table "permissions_instanceacl"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    read :active do
      filter expr(start_time < now() and (is_nil(end_time) or end_time > now()))
      # hardcoded for now to only show lead authority stuff
      filter expr(grant_type == "SERVICE")
    end

    create :create do
      argument :instance, :map, allow_nil?: false
      argument :user, :map, allow_nil?: false

      change manage_relationship(:instance, type: :append)
      change manage_relationship(:user, type: :append)
    end
  end

  policies do
    policy action(:active) do
      authorize_if relates_to_actor_via(:user, field: :user)
    end

    policy action_type(:create) do
      # Only used in testing right now
      forbid_if always()
    end
  end

  attributes do
    integer_primary_key :id

    attribute :start_time, :datetime do
      default &DateTime.utc_now/0
    end

    attribute :end_time, :datetime

    attribute :grant_type, :string do
      default "SERVICE"
    end

    attribute :access_level_id, :string do
      default "lead-authority"
    end

    create_timestamp :created_at
  end

  relationships do
    belongs_to :user, Ebau.User.User do
      attribute_type :integer
    end

    belongs_to :service, Ebau.User.Service do
      attribute_type :integer
    end

    belongs_to :role, Ebau.User.Role do
      attribute_type :integer
    end

    belongs_to :instance, Ebau.Instances.Instance do
      attribute_type :integer
      allow_nil? false
    end
  end
end
