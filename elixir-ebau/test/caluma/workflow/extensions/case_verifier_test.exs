defmodule Caluma.Workflow.Extensions.Case.VerifierTest do
  use ExUnit.Case, async: true

  @resource_head """
  use Ash.Resource,
    otp_app: :ebau,
    domain: nil,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Workflow.Extensions.Case]

  postgres do
    table "caluma_workflow_case"
    repo Ebau.Repo
    migrate? false
  end

  attributes do
    uuid_primary_key :id
    attribute :document_id, :uuid
  end

  relationships do
    belongs_to :document, Caluma.Form.Document
  end

  caluma_case do
    caluma_document do
      answer :title, :string, question_id: "title"
    end
  end
  """

  # Spark runs verifiers in `@after_verify`, where the compiler turns a raised
  # `DslError` into a diagnostic instead of an exception.
  defp dsl_errors(name, actions) do
    {_, diagnostics} =
      Code.with_diagnostics(fn ->
        ExUnit.CaptureIO.with_io(:stderr, fn ->
          Code.compile_string("""
          defmodule #{name} do
            #{@resource_head}

            actions do
              #{actions}
            end
          end
          """)
        end)
      end)

    for %{message: message} <- diagnostics, message =~ "Spark.Error.DslError", do: message
  end

  test "accepts names that are both an answer and an argument" do
    assert [] =
             dsl_errors(Caluma.Workflow.Extensions.Case.VerifierTest.Valid, """
             update :update do
               argument :title, :string

               change {Caluma.Form.Changes.SaveDocumentAnswers,
                       answers: [:title], relationship: :document}
             end
             """)
  end

  test "rejects a name that is not a declared answer" do
    assert [error] =
             dsl_errors(Caluma.Workflow.Extensions.Case.VerifierTest.NoAnswer, """
             update :update do
               argument :title, :string
               argument :nope, :string

               change {Caluma.Form.Changes.SaveDocumentAnswers,
                       answers: [:title, :nope], relationship: :document}
             end
             """)

    assert error =~ "action :update: [:nope]"
  end
end
