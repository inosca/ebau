defmodule Caluma.Form.Answer do
  @moduledoc """
  Ash resource for a Caluma form answer (`caluma_form_answer`).

  Partial clone: only the fields needed by the eBau Elixir app are mapped.
  See https://github.com/projectcaluma/caluma for the full upstream model.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer,
    authorizers: [Ash.Policy.Authorizer]

  postgres do
    repo Ebau.Repo
    table "caluma_form_answer"
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
    defaults [:read, :destroy, create: :*, update: :*]
  end

  attributes do
    uuid_primary_key :id

    attribute :value, Caluma.Form.Types.AnswerValue do
      public? true
    end
  end

  aggregates do
    max :max_sort, :answer_documents, :sort
  end

  relationships do
    belongs_to :document, Caluma.Form.Document do
      public? true
      allow_nil? false
    end

    belongs_to :question, Caluma.Form.Question do
      public? true
      allow_nil? false
      attribute_type :string
      destination_attribute :slug
    end

    has_many :answer_documents, Caluma.Form.AnswerDocument

    many_to_many :documents, Caluma.Form.Document do
      through Caluma.Form.AnswerDocument
    end
  end

  identities do
    identity :document_question, [:document_id, :question_id]
  end
end
