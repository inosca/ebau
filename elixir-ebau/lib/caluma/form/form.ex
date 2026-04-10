defmodule Caluma.Form.Form do
  @moduledoc false
  use Ash.Resource, domain: Caluma.Form, data_layer: AshPostgres.DataLayer

  postgres do
    table "caluma_form_form"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    create :create_form do
      accept :*
    end
  end

  attributes do
    attribute :slug, :string do
      allow_nil? false
      writable? true
      primary_key? true
      generated? false
      public? true
    end

    attribute :name, :map do
      public? true
      allow_nil? false
    end

    attribute :is_published?, :boolean do
      source :is_published
      public? true
    end

    attribute :is_archived?, :boolean do
      source :is_archived
      public? true
    end

    attribute :meta, :map do
      public? true
    end
  end

  relationships do
    has_many :documents, Caluma.Form.Document do
      source_attribute :slug
      destination_attribute :form_id
    end

    many_to_many :questions, Caluma.Form.Question do
      through Caluma.Form.FormQuestion
      source_attribute :slug
      source_attribute_on_join_resource :form_id
      destination_attribute :slug
      destination_attribute_on_join_resource :question_id
    end

    has_many :form_questions, Caluma.Form.FormQuestion do
      source_attribute :slug
    end
  end
end
