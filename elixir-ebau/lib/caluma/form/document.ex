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
    authorizers: [Ash.Policy.Authorizer]

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
      authorize_if always()
    end
  end

  actions do
    defaults [:read]

    create :create_document do
      argument :form, :map do
        allow_nil? false
      end

      argument :case, :map

      # this is only required because the family_id has a DEFAULT of gen_random_uuid() in postgres
      change set_attribute(:family_id, nil)
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

  attributes do
    uuid_primary_key :id
  end

  relationships do
    has_one :case, Caluma.Workflow.Case
    belongs_to :family, Caluma.Form.Document

    belongs_to :form, Caluma.Form.Form do
      allow_nil? false
      public? true
      destination_attribute :slug
      source_attribute :form_id
      attribute_type :string
    end

    has_many :answers, Caluma.Form.Answer

    has_many :answer_documents, Caluma.Form.AnswerDocument do
      sort sort: :desc
    end

    many_to_many :parent_answers, Caluma.Form.Answer do
      through Caluma.Form.AnswerDocument
    end
  end
end
