defmodule Caluma.Workflow.Case do
  @moduledoc """
  Ash resource for a Caluma workflow case (`caluma_workflow_case`).

  Partial clone: only the fields needed by the eBau Elixir app are mapped.
  See https://github.com/projectcaluma/caluma for the full upstream model.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Workflow,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "caluma_workflow_case"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:instance]}
    end
  end

  attributes do
    uuid_primary_key :id

    attribute :status, :atom do
      constraints one_of: [:running, :canceled, :completed]
      allow_nil? false
      default :running
    end

    attribute :meta, :map do
      default %{}
    end
  end

  actions do
    defaults [:read, :destroy, update: :*]

    create :create_case do
      argument :workflow, :map, allow_nil?: false

      change manage_relationship(:workflow, type: :append_and_remove)
    end
  end

  relationships do
    belongs_to :document, Caluma.Form.Document
    belongs_to :family, Caluma.Workflow.Case

    belongs_to :workflow, Caluma.Workflow.Workflow do
      allow_nil? false
      attribute_type :string
      destination_attribute :slug
    end

    has_one :instance, Ebau.Instances.Instance
  end
end
