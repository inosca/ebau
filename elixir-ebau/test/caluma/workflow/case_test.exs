defmodule Caluma.Workflow.CaseTest do
  use Ebau.DataCase, async: true

  import Caluma.Test.Fixtures

  setup [:create_workflow, :create_form]

  @opts [authorize?: false, actor: nil]

  test "creates no document when no form is given" do
    caluma_case = Caluma.Workflow.create_case!(%{workflow: %{slug: workflow_slug()}}, @opts)

    assert caluma_case.document_id == nil
  end

  test "creates and links a document when a form is given" do
    caluma_case =
      Caluma.Workflow.create_case!(
        %{workflow: %{slug: workflow_slug()}, document: %{form: %{slug: form_slug()}}},
        @opts
      )

    assert caluma_case.document_id != nil
  end
end
