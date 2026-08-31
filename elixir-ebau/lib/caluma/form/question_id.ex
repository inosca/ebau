defmodule Caluma.Form.QuestionId do
  @moduledoc """
  Resolves a `question_id` spec — a slug, a list of slugs, or a
  `{resolver, opts}` tuple (see `Caluma.Form.Behaviours.SlugResolver`) — to Caluma question
  slugs. A list holds the slugs a question had over time, oldest to newest
  (`["question", "question-v2"]`): reads match any of them, writes go to the
  current one — the last.
  """

  @type spec :: String.t() | [String.t()] | {module(), term()}

  @doc "All slugs the spec stands for, resolver applied, deduplicated."
  @spec slugs(spec()) :: [String.t()]
  def slugs(slug) when is_binary(slug), do: [slug]
  def slugs(slugs) when is_list(slugs), do: Enum.uniq(slugs)
  def slugs({mod, opts}), do: slugs(mod.resolve(opts))

  @doc "The current slug, i.e. the one to write to: the last of `slugs/1`."
  @spec slug(spec()) :: String.t()
  def slug(spec), do: spec |> slugs() |> List.last()
end
