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

  alias Caluma.Form.Validations.SpecMatcher

  @impl true
  def supports(_opts), do: [Ash.ActionInput]

  @impl true
  def init(opts), do: SpecMatcher.init(opts)

  @impl true
  def validate(input, opts, _context) do
    SpecMatcher.validate_action_input(input, opts, :question, &"question #{inspect(&1.slug)}")
  end
end
