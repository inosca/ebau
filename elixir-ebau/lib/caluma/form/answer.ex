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
    defaults [:read]
  end

  attributes do
    uuid_primary_key :id

    attribute :question_id, :string do
      allow_nil? false
    end

    attribute :value, Caluma.Form.Types.AnswerValue
  end

  relationships do
    belongs_to :document, Caluma.Form.Document

    many_to_many :documents, Caluma.Form.Document do
      through Caluma.Form.AnswerDocument
    end
  end
end
