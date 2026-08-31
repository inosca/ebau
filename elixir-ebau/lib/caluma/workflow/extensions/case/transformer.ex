defmodule Caluma.Workflow.Extensions.Case.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  alias Caluma.Form.Extensions.Document
  alias Caluma.Workflow.Extensions.Case
  alias Document.AnswerTransformer

  def transform(dsl_state) do
    through = Spark.Dsl.Transformer.get_option(dsl_state, [:caluma_case], :through)

    dsl_state =
      dsl_state
      |> add_document_entities(through)
      |> add_meta_attributes(through)

    {:ok, dsl_state}
  end

  # When `through` is nil, the resource IS the case, so the parent's document FK
  # is `document_id` directly. Otherwise, traverse `<through>.document_id`.
  defp parent_doc_id_ref(nil), do: %Ash.Query.Ref{attribute: :document_id}

  defp parent_doc_id_ref(through),
    do: %Ash.Query.Ref{relationship_path: [through], attribute: :document_id}

  # -- Entity builders --

  defp add_document_entities(dsl_state, through) do
    entities = Spark.Dsl.Transformer.get_entities(dsl_state, [:caluma_case, :caluma_document])
    AnswerTransformer.add_entities(dsl_state, entities, parent_doc_id_ref(through))
  end

  defp add_meta_attributes(dsl_state, through) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:caluma_case, :meta])
    |> Enum.filter(&is_struct(&1, Case.MetaAttribute))
    |> Enum.reduce(dsl_state, fn meta, dsl ->
      {:ok, dsl} =
        Ash.Resource.Builder.add_new_calculation(
          dsl,
          meta.name,
          meta.type,
          {Caluma.Workflow.Calculations.CaseMeta, key: meta.key, through: through}
        )

      dsl
    end)
  end
end
