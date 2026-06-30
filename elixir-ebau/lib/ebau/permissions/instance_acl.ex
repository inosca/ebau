defmodule Ebau.Permissions.InstanceACL do
  @moduledoc """
  Access control list entry that grants a user access to a specific instance.

  Each record links a user (and optionally a service and role) to an instance
  with a time-bounded validity window (`start_time` / `end_time`). The
  `grant_type` and `access_level_id` fields control what kind of access is
  granted.

  The `:active` read action filters to currently valid ACLs and is used by
  instance policies to check whether the actor can see a given instance.

  Backed by the Django-managed `permissions_instanceacl` table
  (`migrate? false`).

  Fore more information look up the documentation in the django permissions
  application.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.Permissions,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "permissions_instanceacl"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    read :active do
      filter expr(start_time <= now() and (is_nil(end_time) or end_time > now()))
    end

    create :create do
      argument :instance, :map, allow_nil?: false
      argument :user, :map, allow_nil?: false

      change manage_relationship(:instance, type: :append)
      change manage_relationship(:user, type: :append)
    end
  end

  policies do
    policy action_type(:read) do
      # TODO: This only show own, would need to be Ebau.Policies.Checks.HasActiveInstanceACL
      # + All the rules from the permission module.
      authorize_if relates_to_actor_via(:user, field: :user)
      authorize_if relates_to_actor_via(:service, field: :service)
      authorize_if expr(service_group_id == ^actor([:service, :service_group, :id]))
      authorize_if relates_to_actor_via(:role, field: :role)
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

    belongs_to :service_group, Ebau.User.ServiceGroup do
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
