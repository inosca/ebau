defmodule Caluma.Form.Extensions.Document.VerifierTest do
  use ExUnit.Case, async: true

  @resource_head """
  use Ash.Resource,
    otp_app: :ebau,
    domain: nil,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  caluma_document do
    answer :title, :string, question_id: "title"
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
             dsl_errors(Caluma.Form.Extensions.Document.VerifierTest.Valid, """
             update :update do
               argument :title, :string
               change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:title]}
             end
             """)
  end

  test "rejects a name that is not a declared answer" do
    assert [error] =
             dsl_errors(Caluma.Form.Extensions.Document.VerifierTest.NoAnswer, """
             update :update do
               argument :title, :string
               argument :nope, :string
               change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:title, :nope]}
             end
             """)

    assert error =~ "action :update: [:nope]"
  end

  test "rejects a name that is not an argument of the action" do
    assert [error] =
             dsl_errors(Caluma.Form.Extensions.Document.VerifierTest.NoArgument, """
             update :update do
               change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:title]}
             end
             """)

    assert error =~ "action :update: [:title]"
  end
end
