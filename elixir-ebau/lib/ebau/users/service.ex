defmodule Ebau.Users.Service do
  use Ash.Resource, otp_app: :ebau, domain: Ebau.Users, data_layer: AshPostgres.DataLayer

  postgres do
    table "SERVICE"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]
  end

  attributes do
    attribute :id, :integer,
      primary_key?: true,
      allow_nil?: false,
      public?: true,
      source: :SERVICE_ID

    attribute :name, :string,
      constraints: [max_length: 100],
      source: :NAME

    attribute :sort, :integer do
      default 0
      allow_nil? false
      source :SORT
    end

    attribute :service_group_id, :integer do
      allow_nil? false
      source :SERVICE_GROUP_ID
    end
  end

  relationships do
    has_many :gis_links, Ebau.Instances.GisLinks
    has_many :groups, Ebau.User.Group
  end
end
