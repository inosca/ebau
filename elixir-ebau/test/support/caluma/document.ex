defmodule Caluma.Test.Document do
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

  @answers [:title, :is_paper, :tags]

  actions do
    defaults [:read]

    create :create do
      argument :form, :map, allow_nil?: false
      argument :title, :string
      argument :is_paper, :boolean
      argument :tags, {:array, :string}

      change Caluma.Form.Changes.SetRootFamily
      change manage_relationship(:form, type: :append)
      change {Caluma.Form.Changes.SaveDocumentAnswers, answers: @answers}
    end

    update :update do
      argument :title, :string
      argument :is_paper, :boolean
      argument :tags, {:array, :string}

      change {Caluma.Form.Changes.SaveDocumentAnswers, answers: @answers}
    end
  end

  caluma_document do
    answer :title, :string, question_id: "title"

    mapped_answer :is_paper, :boolean,
      question_id: "is-paper",
      mapping: %{"is-paper-yes" => true, "is-paper-no" => false}

    mapped_list_answer :tags, :string,
      question_id: "tags",
      mapping: %{"tag-a" => "A", "tag-b" => "B"}

    table :rows, Caluma.Test.Row, question_id: "rows"
  end
end
