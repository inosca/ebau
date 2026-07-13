defmodule Ebau.Core.Resource do
  @moduledoc """
  Legacy `RESOURCE` table — application resources/modules keyed by role ACLs.
  """

  use Ash.Resource,
    domain: Ebau.Core,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer,
    primary_read_warning?: false

  postgres do
    table "RESOURCE"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    read :read do
      primary? true
      prepare build(sort: :sort)
    end
  end

  policies do
    policy action(:read) do
      authorize_if relates_to_actor_via([:roles, :groups], field: :group)
    end
  end

  attributes do
    attribute :id, :integer do
      primary_key? true
      allow_nil? false
      sortable? true
      public? true
      source :RESOURCE_ID
    end

    attribute :name_untranslated, :string do
      allow_nil? true
      constraints max_length: 100
      source :NAME
    end

    attribute :description, :string do
      allow_nil? true
      constraints max_length: 1000
      source :DESCRIPTION
    end

    attribute :template, :string do
      allow_nil? true
      constraints max_length: 500
      source :TEMPLATE
    end

    attribute :class_field, :string do
      allow_nil? true
      constraints max_length: 250
      source :CLASS
    end

    attribute :hidden, :integer do
      allow_nil? false
      constraints min: 0
      source :HIDDEN
    end

    attribute :sort, :integer do
      allow_nil? false
      constraints min: 0
      source :SORT
    end

    attribute :available_resource, :string do
      allow_nil? false
      constraints max_length: 25
      source :AVAILABLE_RESOURCE_ID
    end
  end

  relationships do
    has_many :trans, Ebau.Core.ResourceT

    many_to_many :roles, Ebau.User.Role do
      through Ebau.Core.RRoleAcl
    end
  end

  calculations do
    calculate :name, :string, Ebau.Calculations.LocalisedName
    calculate :link, :string, Ebau.Core.Calculations.Link
  end

  preparations do
    prepare build(load: :name)
  end
end
