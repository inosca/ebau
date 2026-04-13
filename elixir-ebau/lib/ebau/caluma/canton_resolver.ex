defmodule Ebau.Caluma.CantonResolver do
  @moduledoc """
  Resolves question IDs (and answer mappings) based on the current canton.

  Looks up `mapping[canton]` from the Ash context, falling back to
  `mapping[:default]`. The canton is read from `context.canton` or
  `context.source_context.canton`.

  ## Usage

      caluma_document do
        answer :name, :string,
          question_id: {Ebau.Caluma.CantonResolver, %{default: "nachname", gr: "familienname"}}

        mapped_answer :is_paper, :boolean,
          question_id: {Ebau.Caluma.CantonResolver, %{default: "is-paper"}},
          mapping:
            {Ebau.Caluma.CantonResolver,
             %{
               default: %{"is-paper-yes" => true, "is-paper-no" => false},
               so: %{"ist-papier-ja" => true, "ist-papier-nein" => false}
             }}
      end
  """

  @behaviour Caluma.Form.QuestionIdResolver

  @impl true
  def resolve(mapping, context) do
    canton = get_canton(context)
    result = if canton, do: mapping[canton] || mapping[:default], else: mapping[:default]

    result ||
      raise "CantonResolver: no mapping for canton #{inspect(canton)} and no :default in #{inspect(Map.keys(mapping))}"
  end

  defp get_canton(%{canton: canton}), do: canton
  defp get_canton(%{source_context: %{canton: canton}}), do: canton
  defp get_canton(_context), do: nil
end
