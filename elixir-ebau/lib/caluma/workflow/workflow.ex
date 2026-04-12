defmodule Caluma.Workflow.Workflow do
  @moduledoc """
  Ash resource for a Caluma workflow definition (`caluma_workflow_workflow`).

  Partial clone: only the fields needed by the eBau Elixir app are mapped.
  See https://github.com/projectcaluma/caluma for the full upstream model.
  """

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

    attribute :name, Caluma.Form.Types.LocalizedField, allow_nil?: false, public?: true
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
