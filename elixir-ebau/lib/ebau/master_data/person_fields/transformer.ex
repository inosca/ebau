defmodule Ebau.MasterData.PersonFields.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  alias Caluma.Form.Extensions.Document.Answer

  def before?(Caluma.Form.Extensions.Document.AnswerTransformer), do: true
  def before?(_), do: false

  def transform(dsl_state) do
    dsl_state =
      Ebau.MasterData.PersonFields.fields()
      |> Enum.reduce(dsl_state, fn {name, type, question_id}, dsl ->
        entity = %Answer{name: name, type: type, question_id: question_id}
        Spark.Dsl.Transformer.add_entity(dsl, [:caluma_document], entity)
      end)

    {:ok, dsl_state}
  end
end
