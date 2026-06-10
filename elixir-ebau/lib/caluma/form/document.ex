defmodule Caluma.Form.Document do
  @moduledoc """
  Ash resource for a Caluma form document (`caluma_form_document`).

  Partial clone: only the fields needed by the eBau Elixir app are mapped.
  See https://github.com/projectcaluma/caluma for the full upstream model.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer,
    extensions: [Caluma.Form.Extensions.Document]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL,
                    via: [:family, :case, :family, :instance]}

      # TODO: We don't have work items yet, add this once there is a relationship on document.
      # authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:family, :work_item, :case, :family]}
    end
  end

  actions do
    create :create_document do
      argument :form, :map do
        allow_nil? false
      end

      argument :case, :map

      change Caluma.Form.Changes.SetRootFamily
      change manage_relationship(:form, type: :append)
      change manage_relationship(:case, type: :append)
    end

    create :create_row_document do
      argument :document, :map do
        allow_nil? false
      end

      argument :question, :map do
        allow_nil? false
      end

      argument :answers, {:array, :map}

      change manage_relationship(:answers, type: :create)
      change Caluma.Form.Changes.CreateRowDocument
    end
  end

  relationships do
    has_one :case, Caluma.Workflow.Case, domain: Caluma.Workflow

    belongs_to :form, Caluma.Form.Form do
      allow_nil? false
      destination_attribute :slug
      source_attribute :form_id
      attribute_type :string
    end

    many_to_many :parent_answers, Caluma.Form.Answer do
      through Caluma.Form.AnswerDocument
    end
  end
end
