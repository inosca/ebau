defmodule Caluma.Form.Validations.EnsureFixtureFormQuestionMatches do
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
