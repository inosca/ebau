defmodule Caluma.Form.AnswerDocument do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer

  alias Caluma.Form.Answer
  alias Caluma.Form.Document

  postgres do
    table "caluma_form_answerdocument"
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
    belongs_to :answer, Answer
    belongs_to :document, Document
  end
end
