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
  end

  relationships do
    belongs_to :form, Caluma.Form.Form,
      primary_key?: true,
      allow_nil?: false,
      destination_attribute: :slug,
      attribute_type: :string

    belongs_to :question, Caluma.Form.Question,
      primary_key?: true,
      allow_nil?: false,
      destination_attribute: :slug,
      attribute_type: :string
  end
end
