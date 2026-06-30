defmodule Caluma.Workflow.Extensions.Case do
  @moduledoc """
  Ash extension for resources that are (or relate to) a Caluma case.

  Provides a `caluma_case` DSL section with nested `caluma_document` and
  `meta` subsections for declaring calculations and relationships that
  read from the case's document answers and meta JSON.

  The `caluma_document` subsection reuses the same entity types as
  `Caluma.Form.Extensions.Document` — `answer`, `mapped_answer`,
  `mapped_list_answer`, and `table`.

  ## Usage

  When the resource IS a Caluma case (or has a direct `document` relationship):

      use Ash.Resource,
        extensions: [Caluma.Workflow.Extensions.Case]

      caluma_case do
        caluma_document do
          answer :proposal, :string, question_id: "umschreibung-bauprojekt"
        end

        meta do
          attribute :dossier_number, :string, key: "dossier-number"
        end
      end

  When the resource relates to a case through a relationship:

      caluma_case do
        through :case  # relationship name pointing to the Caluma case

        caluma_document do
          answer :proposal, :string, question_id: "umschreibung-bauprojekt"
        end
      end

  ## The `through` option

  When omitted, the extension assumes the resource itself is (or acts as)
  a Caluma case — answers resolve via `document.answers` and meta via `meta`.

  When specified, it names the relationship that points to the Caluma case.
  Answers then resolve through `<rel>.document.answers` and meta through
  `<rel>.meta`.

  ## The `question_id` and `key` options

  These accept the same forms as `Caluma.Form.Extensions.Document` — a
  plain string, a list of strings, or a `{resolver_module, opts}` tuple.
  See `Caluma.Form.QuestionIdResolver`.

  ## The `mapping` option

  For `mapped_answer` and `mapped_list_answer`, the `mapping` option
  accepts either a flat `%{string => value}` map or a `{resolver_module, opts}`
  tuple for dynamic resolution at query time.
  """

  # -- Case-specific entity --

  defmodule MetaAttribute do
    @moduledoc false
    defstruct [:name, :type, :key, __spark_metadata__: nil]
  end

  # -- Meta entity definition --

  @meta_attribute %Spark.Dsl.Entity{
    name: :attribute,
    describe: "Declares a calculation that reads from the case's meta JSON.",
    target: MetaAttribute,
    schema: [
      name: [type: :atom, required: true, doc: "The calculation name."],
      type: [type: :atom, required: true, doc: "The Ash type for this calculation."],
      key: [
        type: {:or, [:string, :mod_arg]},
        required: true,
        doc:
          "A meta key string or a {resolver_module, opts} tuple. See `Caluma.Form.QuestionIdResolver`."
      ]
    ],
    args: [:name, :type]
  }

  # -- Section definitions --
  # Reuse entity definitions from Document extension

  @caluma_document %Spark.Dsl.Section{
    name: :caluma_document,
    describe: "Declares answers and tables from the case's document.",
    entities: [
      Caluma.Form.Extensions.Document.answer_entity(),
      Caluma.Form.Extensions.Document.mapped_answer_entity(),
      Caluma.Form.Extensions.Document.mapped_list_answer_entity(),
      Caluma.Form.Extensions.Document.table_entity()
    ]
  }

  @meta %Spark.Dsl.Section{
    name: :meta,
    describe: "Declares attributes from the case's meta JSON.",
    entities: [@meta_attribute]
  }

  @caluma_case %Spark.Dsl.Section{
    name: :caluma_case,
    describe: "Declares Caluma case data accessible through a relationship.",
    schema: [
      through: [
        type: :atom,
        doc:
          "The relationship name that points to the Caluma case. When omitted, the resource itself is treated as the case."
      ]
    ],
    sections: [@caluma_document, @meta]
  }

  use Spark.Dsl.Extension,
    sections: [@caluma_case],
    transformers: [Caluma.Workflow.Extensions.Case.Transformer]
end

defmodule Caluma.Workflow.Extensions.Case.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  require Ash.Expr

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
    source = Spark.Dsl.Transformer.get_persisted(dsl_state, :module)
    doc_id_ref = parent_doc_id_ref(through)

    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:caluma_case, :caluma_document])
    |> Enum.reduce(dsl_state, fn
      %Document.Answer{} = answer, dsl ->
        rel_name = AnswerTransformer.answer_relationship_name(answer.name)

        dsl
        |> AnswerTransformer.add_answer_relationship(rel_name, answer.question_id, doc_id_ref)
        |> AnswerTransformer.add_calc(
          answer.name,
          answer.type,
          Caluma.Form.Calculations.DocumentAnswer,
          relationship: rel_name
        )

      %Document.MappedAnswer{} = mapped, dsl ->
        rel_name = AnswerTransformer.answer_relationship_name(mapped.name)

        dsl
        |> AnswerTransformer.add_answer_relationship(rel_name, mapped.question_id, doc_id_ref)
        |> AnswerTransformer.add_calc(
          mapped.name,
          mapped.type,
          Caluma.Form.Calculations.MappedDocumentAnswer,
          relationship: rel_name,
          mapping: mapped.mapping
        )

      %Document.MappedListAnswer{} = mapped, dsl ->
        rel_name = AnswerTransformer.answer_relationship_name(mapped.name)

        dsl
        |> AnswerTransformer.add_answer_relationship(rel_name, mapped.question_id, doc_id_ref)
        |> AnswerTransformer.add_calc(
          mapped.name,
          {:array, mapped.type},
          Caluma.Form.Calculations.MappedListDocumentAnswer,
          relationship: rel_name,
          mapping: mapped.mapping
        )

      %Document.Table{} = table, dsl ->
        AnswerTransformer.add_table_relationship(dsl, table, source, doc_id_ref)

      _, dsl ->
        dsl
    end)
  end

  defp add_meta_attributes(dsl_state, through) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:caluma_case, :meta])
    |> Enum.filter(&is_struct(&1, Case.MetaAttribute))
    |> Enum.reduce(dsl_state, fn meta, dsl ->
      {:ok, calc} =
        Ash.Resource.Builder.build_calculation(
          meta.name,
          meta.type,
          {Caluma.Workflow.Calculations.CaseMeta, key: meta.key, through: through}
        )

      Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
    end)
  end
end
