defmodule Caluma.Form.Validations.ExistingFormQuestionMatchesSpec do
  @moduledoc """
  Validates that an already persisted form-question join matches requested spec.

  Used by `Caluma.Form.FormQuestion.assert_form_question_compatible` when
  form tree references question already attached to form. Right now only `sort`
  is checked because that is only mutable field managed by form-tree sync.
  """

  use Ash.Resource.Validation

  alias Ash.ActionInput
  alias Ash.Error.Action.InvalidArgument

  @impl true
  def supports(_opts), do: [Ash.ActionInput]

  @impl true
  def validate(input, _opts, _context) do
    sort = ActionInput.get_argument(input, :sort)
    form_question = ActionInput.get_argument(input, :form_question)

    if form_question.sort == sort do
      :ok
    else
      {:error,
       InvalidArgument.exception(
         field: :sort,
         value: sort,
         message:
           "form question #{inspect(form_question.id)} already exists with sort=#{inspect(form_question.sort)}, got #{inspect(sort)}"
       )}
    end
  end
end
