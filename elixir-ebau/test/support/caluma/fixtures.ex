defmodule Caluma.Test.Fixtures do
  @moduledoc """
  ExUnit setup callbacks for generic Caluma tests. Everything goes through
  real domain actions:

      import Caluma.Test.Fixtures

      setup [:create_workflow, :create_form, :create_document]
  """

  alias Caluma.Form.Extensions.Document
  alias Caluma.Form.Extensions.Document.Info
  alias Caluma.Form.QuestionId

  @opts [authorize?: false, actor: nil]
  @workflow "test-workflow"
  @form "test-form"

  def workflow_slug, do: @workflow
  def form_slug, do: @form

  def create_workflow(_context) do
    create_workflow!(@workflow)
    :ok
  end

  def create_workflow!(slug) do
    Caluma.Workflow.create_workflow!(%{slug: slug, name: %{"de" => slug}}, @opts)
  end

  def create_form(_context) do
    create_form!(@form, Caluma.Test.Document)
    :ok
  end

  @doc """
  Creates form `slug` with one question per `caluma_document` entity that
  `resource` declares, under the slugs `Caluma.Form.QuestionId.slug/1`
  resolves. Tables recurse into their row resource.
  """
  def create_form!(slug, resource) do
    Caluma.Form.create_form_tree!(
      %{slug: slug, name: slug, questions: questions(resource)},
      @opts
    )
  end

  def create_document(_context), do: %{document: create_document!()}

  @doc """
  Creates a `Caluma.Test.Document` on the test form. Params (e.g.
  `title: "x"`) pass through to the create action.
  """
  def create_document!(params \\ %{}) do
    Caluma.Test.Domain.create_document!(
      Map.merge(%{form: %{slug: @form}}, Map.new(params)),
      @opts
    )
  end

  defp questions(resource), do: resource |> Info.caluma_document() |> Enum.map(&question/1)

  defp question(%Document.Table{} = table) do
    slug = slug(table.question_id)

    %{
      slug: slug,
      label: slug,
      type: :table,
      form: %{slug: "#{slug}-row-form", name: "#{table.name} row form"},
      questions: questions(table.resource)
    }
  end

  defp question(%Document.Answer{type: type} = answer) when type in [:integer, :float] do
    slug = slug(answer.question_id)
    %{slug: slug, label: slug, type: type}
  end

  defp question(%Document.Answer{} = answer) do
    slug = slug(answer.question_id)
    %{slug: slug, label: slug, type: :text}
  end

  defp question(%Document.MappedAnswer{} = answer) do
    slug = slug(answer.question_id)
    %{slug: slug, label: slug, type: :choice}
  end

  defp question(%Document.MappedListAnswer{} = answer) do
    slug = slug(answer.question_id)
    %{slug: slug, label: slug, type: :multiple_choice}
  end

  defp slug(question_id), do: QuestionId.slug(question_id)
end
