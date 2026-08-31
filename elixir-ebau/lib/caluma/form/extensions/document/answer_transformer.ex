defmodule Caluma.Form.Extensions.Document.AnswerTransformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  require Ash.Expr

  alias Caluma.Form.Extensions.Document
  alias Caluma.Form.QuestionId

  # The resource IS the document, so the parent's primary key is `id`.
  @parent_doc_id_ref %Ash.Query.Ref{attribute: :id}

  def transform(dsl_state) do
    entities = Spark.Dsl.Transformer.get_entities(dsl_state, [:caluma_document])
    {:ok, add_entities(dsl_state, entities, @parent_doc_id_ref)}
  end

  @doc """
  Adds a relationship (plus a calculation for answers) per `caluma_document`
  entity. `parent_doc_id_ref` points at the parent document's id on the
  resource.
  """
  def add_entities(dsl_state, entities, parent_doc_id_ref) do
    Enum.reduce(entities, dsl_state, fn
      %Document.Table{} = table, dsl ->
        add_table_relationship(dsl, table, parent_doc_id_ref)

      %{name: name, question_id: question_id} = entity, dsl ->
        rel_name = answer_relationship_name(name)
        {type, calc} = calculation(entity, rel_name)

        dsl
        |> add_answer_relationship(rel_name, question_id, parent_doc_id_ref)
        |> add_calc(name, type, calc)
    end)
  end

  defp calculation(%Document.Answer{type: type}, rel_name),
    do: {type, {Caluma.Form.Calculations.DocumentAnswer, relationship: rel_name}}

  defp calculation(%Document.MappedAnswer{type: type, mapping: mapping}, rel_name),
    do:
      {type,
       {Caluma.Form.Calculations.MappedDocumentAnswer, relationship: rel_name, mapping: mapping}}

  defp calculation(%Document.MappedListAnswer{type: type, mapping: mapping}, rel_name),
    do:
      {{:array, type},
       {Caluma.Form.Calculations.MappedListDocumentAnswer,
        relationship: rel_name, mapping: mapping}}

  defp add_calc(dsl, name, type, calc) do
    {:ok, dsl} = Ash.Resource.Builder.add_new_calculation(dsl, name, type, calc)
    dsl
  end

  def answer_relationship_name(name), do: :"_#{name}_answer"

  defp add_answer_relationship(dsl, rel_name, question_id, parent_doc_id_ref) do
    add_filtered_relationship(dsl, :has_one, rel_name, Caluma.Form.Answer, [],
      filter: answer_filter(parent_doc_id_ref, question_id)
    )
  end

  defp add_table_relationship(dsl, table, parent_doc_id_ref) do
    add_filtered_relationship(dsl, :has_many, table.name, table.resource, [sort: [sort: :desc]],
      filter: table_filter(parent_doc_id_ref, table.question_id)
    )
  end

  # `filter` is not a relationship DSL option, so set it on the built struct.
  defp add_filtered_relationship(dsl, type, name, destination, opts, filter: filter) do
    {:ok, rel} =
      Ash.Resource.Builder.build_relationship(
        type,
        name,
        destination,
        Keyword.put(opts, :no_attributes?, true)
      )

    Spark.Dsl.Transformer.add_entity(dsl, [:relationships], %{rel | filter: filter})
  end

  # Both filters match any slug the `question_id` resolves to. A single slug
  # filters with `question_id ==`, which is more efficient on big data sets
  # than `question_id in`.
  defp answer_filter(parent_doc_id_ref, question_id) do
    case QuestionId.slugs(question_id) do
      [slug] ->
        Ash.Expr.expr(document_id == parent(^parent_doc_id_ref) and question_id == ^slug)

      slugs ->
        Ash.Expr.expr(document_id == parent(^parent_doc_id_ref) and question_id in ^slugs)
    end
  end

  # Selects the row documents in the parent's family under the table question.
  defp table_filter(parent_doc_id_ref, question_id) do
    case QuestionId.slugs(question_id) do
      [slug] ->
        Ash.Expr.expr(
          family.id == parent(^parent_doc_id_ref) and
            exists(answer_documents, answer.question_id == ^slug)
        )

      slugs ->
        Ash.Expr.expr(
          family.id == parent(^parent_doc_id_ref) and
            exists(answer_documents, answer.question_id in ^slugs)
        )
    end
  end
end
