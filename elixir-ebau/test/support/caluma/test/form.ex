defmodule Caluma.Test.Form do
  @moduledoc """
  Test-only helper for building Caluma form trees inline.

  This creates forms, questions, and form-question joins from nested keyword data.
  Nested `:form` and `:table` questions create nested forms automatically.

  Root question slugs are used as given. Nested question slugs are prefixed with
  their parent generated form slug unless they already contain a dot.

  Generated nested form slugs follow Caluma-style convention and default to the
  resolved question slug.

  ## Examples

      Caluma.Test.Form.create_form!("example-form",
        questions: [
          [slug: "question-1", type: :text],
          [
            slug: "sub-form",
            type: :form,
            questions: [
              [slug: "nested-question", type: :text]
            ]
          ]
        ]
      )
  """

  @type form_slug :: String.t()
  @type question_spec :: keyword()

  @spec create_form!(form_slug(), keyword()) :: Caluma.Form.Form.t()
  def create_form!(slug, opts \\ []) do
    create_form_tree!(slug, opts, nested?: false)
  end

  defp create_form_tree!(slug, opts, nested?: nested?) do
    form =
      Caluma.Form.create_form!(
        %{
          slug: slug,
          name: Keyword.get(opts, :name, default_label(slug)),
          meta: Keyword.get(opts, :meta, %{})
        },
        authorize?: false
      )

    opts
    |> Keyword.get(:questions, [])
    |> Enum.with_index(1)
    |> Enum.each(fn {question_spec, sort} ->
      create_question!(form.slug, question_spec, sort, nested?: nested?)
    end)

    form
  end

  defp create_question!(form_slug, question_spec, sort, nested?: nested?) do
    slug = resolve_question_slug(form_slug, fetch!(question_spec, :slug), nested?)
    type = normalize_type(fetch!(question_spec, :type))
    nested_form_slug = nested_form_slug(type, slug, question_spec)

    if nested_form_slug do
      create_form_tree!(nested_form_slug, question_spec, nested?: true)
    end

    Caluma.Form.create_question!(
      %{
        slug: slug,
        label: Keyword.get(question_spec, :label, default_label(slug)),
        type: type,
        is_hidden: Keyword.get(question_spec, :is_hidden, "false"),
        configuration: Keyword.get(question_spec, :configuration, %{}),
        meta: Keyword.get(question_spec, :meta, %{}),
        row_form_id: if(type == :table, do: nested_form_slug),
        sub_form_id: if(type == :form, do: nested_form_slug)
      },
      authorize?: false
    )

    Caluma.Form.create_form_question!(
      %{
        form_id: form_slug,
        question_id: slug,
        sort: sort
      },
      authorize?: false
    )
  end

  defp nested_form_slug(type, slug, question_spec) when type in [:form, :table] do
    Keyword.get(question_spec, :form_slug, slug)
  end

  defp nested_form_slug(_type, _slug, _question_spec), do: nil

  defp resolve_question_slug(_form_slug, slug, false), do: slug

  defp resolve_question_slug(form_slug, slug, true) do
    if String.contains?(slug, ".") do
      slug
    else
      "#{form_slug}.#{slug}"
    end
  end

  defp normalize_type(:string), do: :text
  defp normalize_type(type), do: type

  defp default_label(slug), do: %{"de" => slug}

  defp fetch!(keyword, key) do
    Keyword.fetch!(keyword, key)
  end
end
