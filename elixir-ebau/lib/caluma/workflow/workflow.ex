defmodule Caluma.Workflow.Workflow do
  @moduledoc false
  use Ash.Resource, domain: Caluma.Workflow, data_layer: AshPostgres.DataLayer

  postgres do
    table "caluma_workflow_workflow"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]
  end

  attributes do
    attribute :slug, :string do
      public? true
      writable? true
      primary_key? true
      allow_nil? false
      always_select? true
      generated? false
    end

    attribute :name, :map, allow_nil?: false, public?: true
  end

  relationships do
    has_many :cases, Caluma.Workflow.Case do
      source_attribute :slug
    end
  end

  identities do
    identity :slug, [:slug]
  end
end
