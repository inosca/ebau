defmodule Caluma.Form.FormQuestion do
  @moduledoc false
  use Ash.Resource, domain: Caluma.Form, data_layer: AshPostgres.DataLayer

  postgres do
    table "caluma_form_formquestion"
    repo Ebau.Repo
    migrate? false

    references do
      reference :form, on_delete: :delete
      reference :question, on_delete: :delete
    end
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]

    create :create_form_question do
      accept [:form_id, :question_id, :sort]
      change Caluma.Form.Changes.SetFormQuestionNaturalKey
    end
  end

  attributes do
    attribute :id, :string do
      allow_nil? false
      writable? true
      primary_key? true
      public? true
    end

    attribute :sort, :integer do
      allow_nil? false
      public? true
    end
  end

  relationships do
    belongs_to :form, Caluma.Form.Form do
      allow_nil? false
      destination_attribute :slug
      attribute_type :string
    end

    belongs_to :question, Caluma.Form.Question do
      allow_nil? false
      destination_attribute :slug
      attribute_type :string
    end
  end

  identities do
    identity :form_question, [:form_id, :question_id]
  end
end
