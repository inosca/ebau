defmodule Ebau.Calculations.LocalisedName do
  @moduledoc """
  Resolves the `:name` of a resource with a legacy `*_T` translation table.

  Picks the translation row matching the locale from the action's scope
  (see `Ebau.Scope`), falling back to the untranslated `name_untranslated`
  attribute when no translation exists.
  """

  use Ash.Resource.Calculation

  @impl true
  def expression(_opts, context) do
    locale = context.source_context[:locale] || Ebau.Scope.default_locale()

    translation = expr(first(trans, query: [filter: language == ^locale], field: :name))

    expr(
      if is_nil(^translation) do
        name_untranslated
      else
        ^translation
      end
    )
  end
end
