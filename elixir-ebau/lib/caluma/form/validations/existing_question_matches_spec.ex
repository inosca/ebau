defmodule Caluma.Form.Validations.ExistingQuestionMatchesSpec do
  @moduledoc """
  Validates that an already persisted question matches a provided form-tree spec.

  Used by `Caluma.Form.Question.assert_question_compatible`. Only arguments
  explicitly present on action input are checked. For localized fields like
  `label`, comparison only checks locales present in provided input.
  """

  use Ash.Resource.Validation

  alias Ash.ActionInput
  alias Ash.Error.Action.InvalidArgument
  alias Caluma.Form.Types.LocalizedFieldHelpers

  @impl true
  def supports(_opts), do: [Ash.ActionInput]

  @impl true
  def validate(input, _opts, _context) do
    with :ok <- validate_field(input, :type, ActionInput.get_argument(input, :type)),
         :ok <- validate_optional_argument(input, :label),
         :ok <- validate_optional_argument(input, :is_hidden),
         :ok <- validate_optional_argument(input, :configuration),
         :ok <- validate_optional_argument(input, :meta),
         :ok <- validate_optional_argument(input, :row_form_id) do
      validate_optional_argument(input, :sub_form_id)
    end
  end

  defp validate_optional_argument(input, field) do
    case ActionInput.fetch_argument(input, field) do
      {:ok, value} -> validate_field(input, field, value)
      :error -> :ok
    end
  end

  defp validate_field(input, :label, value) do
    question = ActionInput.get_argument(input, :question)
    actual = question.label
    expected = LocalizedFieldHelpers.normalize(value)

    if LocalizedFieldHelpers.matches?(actual, expected) do
      :ok
    else
      {:error,
       InvalidArgument.exception(
         field: :label,
         value: value,
         message:
           "question #{inspect(question.slug)} already exists with label #{inspect(actual)}, got #{inspect(expected)}"
       )}
    end
  end

  defp validate_field(input, field, value) do
    question = ActionInput.get_argument(input, :question)
    actual = Map.fetch!(question, field)

    if actual == value do
      :ok
    else
      {:error,
       InvalidArgument.exception(
         field: field,
         value: value,
         message:
           "question #{inspect(question.slug)} already exists with #{field}=#{inspect(actual)}, got #{inspect(value)}"
       )}
    end
  end
end
