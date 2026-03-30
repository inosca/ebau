defmodule Caluma.Form.Document do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]
  end

  attributes do
    uuid_primary_key :id
  end

  relationships do
    has_one :case, Caluma.Workflow.Case
    belongs_to :family, Caluma.Form.Document
    has_many :answers, Caluma.Form.Answer
    has_many :answer_documents, Caluma.Form.AnswerDocument
  end
end
