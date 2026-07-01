defmodule Caluma.Form.Calculations.MappedDocumentAnswer do
  @moduledoc """
  Calculation that extracts an answer from a Caluma document and maps its
  value using a provided mapping.

  The transformer passes a `relationship` option naming a filtered
  `has_one` relationship to `Caluma.Form.Answer` (one per declared answer).

  The `mapping` option accepts either a flat `%{string => value}` map or
  a `{resolver_module, opts}` tuple (see `Caluma.Form.Resolver`).
  """

  use Ash.Resource.Calculation

  import Ash.Expr

  alias Caluma.Form.Calculations.DocumentAnswer

  @impl true
  defdelegate init(opts), to: DocumentAnswer, as: :init_with_mapping

  @impl true
  def expression(opts, _context) do
    mapping = DocumentAnswer.resolve_mapping(opts[:mapping])
    # TODO only supports text questions for now
    answer_expr = DocumentAnswer.answer_expr(opts[:relationship], :value_string)

    Enum.reduce(mapping, expr(nil), fn {answer_value, mapped_value}, acc ->
      expr(
        if ^answer_expr == ^answer_value do
          ^mapped_value
        else
          ^acc
        end
      )
    end)
  end
end
