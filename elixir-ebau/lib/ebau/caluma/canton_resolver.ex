defmodule Ebau.Caluma.CantonResolver do
  # `question_id` resolvers are invoked inside a compile-time Spark transformer
  # (`Caluma.Form.Extensions.Document.AnswerTransformer`), which bakes the
  # resolved slug into the resource's relationship filter. The canton must
  # therefore be a compile-time value: read it with `compile_env` (not
  # `get_env`) so a build-vs-runtime canton mismatch is caught at boot instead
  # of silently querying with the wrong slug.
  @canton Application.compile_env(:ebau, :canton)

  @moduledoc """
  Resolves question IDs (and answer mappings) based on the canton this build
  was compiled for.

  Looks up `mapping[canton]`, falling back to `mapping[:default]`. The canton
  is fixed at compile time (see the `@canton` module attribute), so a
  given build only ever resolves for a single canton.

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

  @behaviour Caluma.Form.Resolver

  @impl true
  def resolve(mapping) do
    canton = @canton
    result = if canton, do: mapping[canton] || mapping[:default], else: mapping[:default]

    result ||
      raise "CantonResolver: no mapping for canton #{inspect(canton)} and no :default in #{inspect(Map.keys(mapping))}"
  end
end
