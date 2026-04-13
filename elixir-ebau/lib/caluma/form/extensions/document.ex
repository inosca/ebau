defmodule Caluma.Form.Extensions.Document do
  @moduledoc """
  Ash extension that adds the standard Caluma document fields to a resource
  backed by the `caluma_form_document` table.

  Adds:
  - `uuid_primary_key :id`
  - `has_many :answers` (Caluma.Form.Answer, via document_id)
  - `has_many :answer_documents` (Caluma.Form.AnswerDocument)
  - `belongs_to :family` (Caluma.Form.Document)
  - `defaults [:read]` action

  The target resource must define its own `postgres do` block with table, repo,
  and `migrate? false`.

  ## Usage

      defmodule MyApp.SomeDocumentView do
        use Ash.Resource,
          otp_app: :ebau,
          domain: MyApp.SomeDomain,
          data_layer: AshPostgres.DataLayer,
          extensions: [Caluma.Form.Extensions.Document]
      end
  """

  use Spark.Dsl.Extension,
    transformers: [Caluma.Form.Extensions.Document.Transformer]
end

defmodule Caluma.Form.Extensions.Document.Transformer do
  use Spark.Dsl.Transformer

  def transform(dsl_state) do
    {:ok, dsl_state} = add_action(dsl_state)
    {:ok, dsl_state} = add_attribute(dsl_state)
    {:ok, dsl_state} = add_aggregates(dsl_state)
    {:ok, dsl_state} = add_relationships(dsl_state)

    {:ok, dsl_state}
  end

  defp add_action(dsl_state) do
    {:ok, action} =
      Spark.Dsl.Transformer.build_entity(Ash.Resource.Dsl, [:actions], :read,
        name: :read,
        primary?: true
      )

    {:ok, Spark.Dsl.Transformer.add_entity(dsl_state, [:actions], action)}
  end

  defp add_attribute(dsl_state) do
    {:ok, attr} =
      Spark.Dsl.Transformer.build_entity(Ash.Resource.Dsl, [:attributes], :uuid_primary_key,
        name: :id
      )

    {:ok, Spark.Dsl.Transformer.add_entity(dsl_state, [:attributes], attr)}
  end

  defp add_aggregates(dsl_state) do
    {:ok, agg} =
      Ash.Resource.Builder.build_aggregate(
        :row_sort,
        :min,
        :answer_documents,
        field: :sort
      )

    {:ok, Spark.Dsl.Transformer.add_entity(dsl_state, [:aggregates], agg)}
  end

  defp add_relationships(dsl_state) do
    {:ok, answers} =
      Ash.Resource.Builder.build_relationship(:has_many, :answers, Caluma.Form.Answer,
        destination_attribute: :document_id
      )

    {:ok, answer_documents} =
      Ash.Resource.Builder.build_relationship(
        :has_many,
        :answer_documents,
        Caluma.Form.AnswerDocument,
        destination_attribute: :document_id
      )

    {:ok, family} =
      Ash.Resource.Builder.build_relationship(:belongs_to, :family, Caluma.Form.Document, [])

    dsl_state =
      dsl_state
      |> Spark.Dsl.Transformer.add_entity([:relationships], answers)
      |> Spark.Dsl.Transformer.add_entity([:relationships], answer_documents)
      |> Spark.Dsl.Transformer.add_entity([:relationships], family)

    {:ok, dsl_state}
  end
end
