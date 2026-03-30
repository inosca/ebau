defmodule Caluma.Workflow.Case do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Workflow,
    data_layer: AshPostgres.DataLayer

  postgres do
    table "caluma_workflow_case"
    repo Ebau.Repo
    migrate? false
  end

  attributes do
    uuid_primary_key :id
    attribute :meta, :map do
      default %{}
    end
  end

  actions do
    defaults [:read]
  end

  relationships do
    belongs_to :document, Caluma.Form.Document
  end
end
