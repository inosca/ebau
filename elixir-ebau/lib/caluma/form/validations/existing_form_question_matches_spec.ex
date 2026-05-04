defmodule Caluma.Form.Validations.ExistingFormQuestionMatchesSpec do
  @moduledoc """
  Validates that one attribute on the form-question passed as the
  `:form_question` argument matches the corresponding action argument.

  Used by `Caluma.Form.assert_form_question_compatible`. Apply once per field
  via the `field:` option.
  """

  use Ash.Resource.Validation

  alias Ash.ActionInput
  alias Ash.Error.Action.InvalidArgument
  alias Caluma.Form.Validations.SpecMatcher

  @impl true
  def supports(_opts), do: [Ash.ActionInput]

  @impl true
  def init(opts) do
    case opts[:field] do
      field when is_atom(field) and not is_nil(field) -> {:ok, opts}
      _ -> {:error, "field option is required (atom)"}
    end
  end

  @impl true
  def validate(input, opts, _context) do
    field = opts[:field]

    case ActionInput.get_argument(input, field) do
      nil ->
        :ok

      value ->
        form_question = ActionInput.get_argument(input, :form_question)

        case SpecMatcher.compare(form_question, field, value) do
          :ok ->
            :ok

          {:mismatch, actual, expected} ->
            {:error,
             InvalidArgument.exception(
               field: field,
               value: value,
               message:
                 "form question #{inspect(form_question.id)} already exists with #{field}=#{inspect(actual)}, got #{inspect(expected)}"
             )}
        end
    end
  end
end
