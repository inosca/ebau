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
    defaults [:read, :destroy, create: :*, update: :*]
  end

  attributes do
    uuid_primary_key :id

    attribute :sort, :integer do
      default 0
    end
  end

  relationships do
    belongs_to :answer, Answer do
      allow_nil? false
    end

    belongs_to :document, Document do
      allow_nil? false
    end
  end
end
