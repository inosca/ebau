defmodule Caluma.Test.Row do
  @moduledoc false

  use Ash.Resource,
    domain: Caluma.Test.Domain,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    create :create do
      argument :parent_id, :uuid, allow_nil?: false
      argument :field, :string

      change {Caluma.Form.Changes.AddTableRow,
              question: {Caluma.Test.Document, :rows}, document_argument: :parent_id}

      change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:field]}
    end

    update :update do
      argument :field, :string

      change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:field]}
    end

    destroy :destroy do
      require_atomic? false

      change cascade_destroy(:answers, after_action?: false, return_notifications?: false)

      change cascade_destroy(:answer_documents,
               after_action?: false,
               return_notifications?: false
             )
    end
  end

  caluma_document do
    answer :field, :string, question_id: "field"
  end
end
