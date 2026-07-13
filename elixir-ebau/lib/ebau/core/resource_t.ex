defmodule Ebau.Core.ResourceT do
  @moduledoc """
  Legacy `RESOURCE_T` translations for `Ebau.Core.Resource`.
  """

  use Ash.Resource, domain: Ebau.Core, data_layer: AshPostgres.DataLayer

  postgres do
    table "RESOURCE_T"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]
  end

  attributes do
    attribute :id, :integer do
      primary_key? true
      allow_nil? false
      sortable? true
      public? true
    end

    attribute :resource_id, :integer do
      allow_nil? false
      public? false
      source :RESOURCE_ID
    end

    attribute :language, :string do
      allow_nil? false
      source :LANGUAGE
      public? true
      constraints max_length: 2
    end

    attribute :name, :string do
      allow_nil? true
      source :NAME
      public? true
      constraints max_length: 100
    end

    attribute :description, :string do
      allow_nil? true
      source :DESCRIPTION
      constraints max_length: 1000
    end
  end

  relationships do
    belongs_to :resource, Ebau.Core.Resource
  end
end
