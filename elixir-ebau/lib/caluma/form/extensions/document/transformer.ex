defmodule Caluma.Form.Extensions.Document.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  def before?(Caluma.Form.Extensions.Document.AnswerTransformer), do: true
  def before?(_), do: false

  def transform(dsl_state) do
    {:ok, id} =
      Spark.Dsl.Transformer.build_entity(Ash.Resource.Dsl, [:attributes], :uuid_primary_key,
        name: :id
      )

    dsl_state = Spark.Dsl.Transformer.add_entity(dsl_state, [:attributes], id)

    {:ok, dsl_state} =
      Ash.Resource.Builder.add_new_aggregate(dsl_state, :sort, :min, :answer_documents,
        field: :sort
      )

    {:ok, add_relationships(dsl_state)}
  end

  # `add_new_relationship` skips relationships the resource declares itself
  # (e.g. `Caluma.Form.Document` declares `:form`).
  @relationships [
    {:has_many, :answers, Caluma.Form.Answer, destination_attribute: :document_id},
    {:has_many, :answer_documents, Caluma.Form.AnswerDocument,
     destination_attribute: :document_id},
    {:belongs_to, :family, Caluma.Form.Document, []},
    {:belongs_to, :form, Caluma.Form.Form, allow_nil?: false, destination_attribute: :slug,
     source_attribute: :form_id, attribute_type: :string},
    {:many_to_many, :parent_answers, Caluma.Form.Answer, through: Caluma.Form.AnswerDocument,
     source_attribute_on_join_resource: :document_id,
     destination_attribute_on_join_resource: :answer_id}
  ]

  defp add_relationships(dsl_state) do
    Enum.reduce(@relationships, dsl_state, fn {type, name, dest, opts}, dsl ->
      {:ok, dsl} = Ash.Resource.Builder.add_new_relationship(dsl, type, name, dest, opts)
      dsl
    end)
  end
end
