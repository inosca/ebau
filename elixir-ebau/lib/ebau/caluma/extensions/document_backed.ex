defmodule Ebau.Caluma.Extensions.DocumentBacked do
  @moduledoc """
  Spark DSL extension that generates DocumentAnswer calculations from a
  declarative `caluma_document` block.

  ## Usage

      use Ash.Resource,
        extensions: [Caluma.Form.Extensions.Document, Ebau.Caluma.Extensions.DocumentBacked]

      caluma_document do
        field :plot_number, :string, question_ids: %{default: "parzellennummer"}
        field :coord_east, :string, question_ids: %{default: "lagekoordinaten-ost", gr: "coordinates-east"}
      end
  """

  defmodule Field do
    @moduledoc false
    defstruct [:name, :type, :question_ids, __spark_metadata__: nil]
  end

  @field %Spark.Dsl.Entity{
    name: :field,
    describe: "Declares a calculation that reads a Caluma document answer by question ID.",
    target: Field,
    schema: [
      name: [
        type: :atom,
        required: true,
        doc: "The calculation name."
      ],
      type: [
        type: :atom,
        required: true,
        doc: "The Ash type (reserved for documentation; AnswerValue is used)."
      ],
      question_ids: [
        type: {:map, :atom, {:or, [:string, {:list, :string}]}},
        required: true,
        doc: "Map of canton atom to question ID(s). Must include :default."
      ]
    ],
    args: [:name, :type]
  }

  @caluma_document %Spark.Dsl.Section{
    name: :caluma_document,
    describe: "Declares document-backed calculations on a resource.",
    entities: [@field]
  }

  use Spark.Dsl.Extension,
    sections: [@caluma_document],
    transformers: [Ebau.Caluma.Extensions.DocumentBacked.Transformer]
end

defmodule Ebau.Caluma.Extensions.DocumentBacked.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  def transform(dsl_state) do
    dsl_state =
      dsl_state
      |> Spark.Dsl.Transformer.get_entities([:caluma_document])
      |> Enum.reduce(dsl_state, fn attr, dsl ->
        {:ok, calc} =
          Ash.Resource.Builder.build_calculation(
            attr.name,
            Caluma.Form.Types.AnswerValue,
            {Ebau.Caluma.Calculations.DocumentAnswer, question_ids: attr.question_ids}
          )

        Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
      end)

    {:ok, dsl_state}
  end
end
