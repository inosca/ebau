defmodule Caluma.Form.Validations.ExistingFormQuestionMatchesSpec do
  @moduledoc """
  Validates that one attribute on the form-question passed as the
  `:form_question` argument matches the corresponding action argument.

  Used by `Caluma.Form.assert_form_question_compatible`. Apply once per field
  via the `field:` option.
  """

  use Ash.Resource.Validation

  alias Caluma.Form.Validations.SpecMatcher

  @impl true
  def supports(_opts), do: [Ash.ActionInput]

  @impl true
  def init(opts), do: SpecMatcher.init(opts)

  @impl true
  def validate(input, opts, _context) do
    SpecMatcher.validate_action_input(
      input,
      opts,
      :form_question,
      &"form question #{inspect(&1.id)}"
    )
  end
end
