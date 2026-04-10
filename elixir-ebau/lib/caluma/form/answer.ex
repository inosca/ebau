defmodule Caluma.Form.Answer do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer

  postgres do
    repo Ebau.Repo
    table "caluma_form_answer"
    migrate? false
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
