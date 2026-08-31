defmodule Caluma.Workflow.Extensions.Case.Verifier do
  @moduledoc false

  use Spark.Dsl.Verifier

  # The answers live under `caluma_case`, the check itself is the Document one.
  def verify(dsl_state) do
    Caluma.Form.Extensions.Document.Verifier.verify_save_document_answers(
      dsl_state,
      Spark.Dsl.Verifier.get_entities(dsl_state, [:caluma_case, :caluma_document])
    )
  end
end
