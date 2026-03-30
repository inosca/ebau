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
  end

  actions do
    defaults [:read, :destroy, create: []]
  end

  attributes do
    uuid_primary_key :id
  end

  relationships do
    belongs_to :answer, Answer do
      # source_attribute :answer_id
      # destination_attribute :id
      # primary_key? false
    end

    belongs_to :document, Document do
      # source_attribute :document_id
      # destination_attribute :id
      # primary_key? false
    end
  end
end
