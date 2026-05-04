defmodule Caluma.Form.Validations.ExistingQuestionMatchesSpec do
  @moduledoc """
  Validates that one attribute on the question passed as the `:question`
  argument matches the corresponding action argument.

  Used by `Caluma.Form.assert_question_compatible`. Apply once per field via
  the `field:` option. A `nil` argument is treated as "no expectation" and
  skipped.

  For the localized `:label` field, comparison considers only locales present
  in the provided value.
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
        question = ActionInput.get_argument(input, :question)

        case SpecMatcher.compare(question, field, value) do
          :ok ->
            :ok

          {:mismatch, actual, expected} ->
            {:error,
             InvalidArgument.exception(
               field: field,
               value: value,
               message:
                 "question #{inspect(question.slug)} already exists with #{field}=#{inspect(actual)}, got #{inspect(expected)}"
             )}
        end
    end
  end
end
