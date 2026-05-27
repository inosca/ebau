defmodule Caluma.Form.Changes.SyncFormTree do
  @moduledoc """
  Synchronizes persisted Caluma form tree with declarative form-tree input.

  Used by `Caluma.Form.create_form_tree` and `Caluma.Form.apply_form_tree`.
  It walks ordered question specs, creates missing nested forms/questions/join rows,
  and asserts compatibility when matching records already exist.
  """

  use Ash.Resource.Change

  alias Ash.Changeset

  @impl true
  def change(changeset, _opts, context) do
    questions = Changeset.get_argument(changeset, :questions) || []
    action_opts = Ash.Context.to_opts(context)

    Changeset.after_action(changeset, fn _changeset, form ->
      create_questions!(form.slug, questions, action_opts)

      {:ok, form}
    end)
  end

  defp create_questions!(form_slug, questions, action_opts) do
    questions
    |> Enum.with_index(1)
    |> Enum.each(fn {question_spec, sort} ->
      create_question!(form_slug, question_spec, sort, action_opts)
    end)
  end

  defp create_question!(form_slug, question_spec, sort, action_opts) do
    slug = Map.fetch!(question_spec, :slug)

    existing_question =
      Caluma.Form.get_question_by_slug!(
        slug,
        Keyword.put(action_opts, :not_found_error?, false)
      )

    type = Map.get(question_spec, :type) || existing_question_type!(existing_question, slug)
    nested_form_attrs = nested_form_attrs(type, slug, question_spec)
    nested_form_slug = nested_form_attrs && nested_form_attrs.slug

    if nested_form_attrs do
      existing_form =
        Caluma.Form.get_form_by_slug!(
          nested_form_attrs.slug,
          Keyword.put(action_opts, :not_found_error?, false)
        )

      if existing_form do
        Caluma.Form.apply_form_tree!(
          existing_form,
          Map.take(nested_form_attrs, [:name, :meta, :questions]),
          action_opts
        )
      else
        Caluma.Form.create_form_tree!(nested_form_attrs, action_opts)
      end
    end

    if existing_question do
      Caluma.Form.assert_question_compatible!(
        existing_question,
        assert_question_input(question_spec, type, nested_form_slug),
        action_opts
      )
    else
      Caluma.Form.create_question!(
        create_question_input(question_spec, type, nested_form_slug),
        action_opts
      )
    end

    create_or_assert_form_question!(form_slug, slug, sort, action_opts)
  end

  defp nested_form_attrs(type, slug, question_spec) when type in [:form, :table] do
    form_attrs = question_spec[:form] || %{}

    %{
      slug: form_attrs[:slug] || slug,
      name: form_attrs[:name],
      meta: form_attrs[:meta] || %{},
      questions: question_spec[:questions] || []
    }
  end

  defp nested_form_attrs(_type, _slug, _question_spec), do: nil

  defp create_or_assert_form_question!(form_slug, question_slug, sort, action_opts) do
    existing_form_question =
      Caluma.Form.get_form_question_by_form_and_question!(
        form_slug,
        question_slug,
        Keyword.put(action_opts, :not_found_error?, false)
      )

    if existing_form_question do
      Caluma.Form.assert_form_question_compatible!(
        existing_form_question,
        sort,
        action_opts
      )
    else
      Caluma.Form.create_form_question!(
        %{form_id: form_slug, question_id: question_slug, sort: sort},
        action_opts
      )
    end
  end

  defp existing_question_type!(nil, slug) do
    raise ArgumentError,
          "question #{inspect(slug)} does not exist yet; type must be provided on first definition"
  end

  defp existing_question_type!(question, _slug), do: question.type

  defp create_question_input(question_spec, type, nested_form_slug) do
    question_spec
    |> Map.take([:slug, :label, :is_hidden, :configuration, :meta])
    |> Map.put(:type, type)
    |> put_nested_form_relationship(type, nested_form_slug)
  end

  defp assert_question_input(question_spec, type, nested_form_slug) do
    question_spec
    |> Map.take([:label, :is_hidden, :configuration, :meta])
    |> Map.put(:type, type)
    |> put_nested_form_id(type, nested_form_slug)
  end

  defp put_nested_form_relationship(input, :table, nested_form_slug)
       when is_binary(nested_form_slug), do: Map.put(input, :row_form, %{slug: nested_form_slug})

  defp put_nested_form_relationship(input, :form, nested_form_slug)
       when is_binary(nested_form_slug), do: Map.put(input, :sub_form, %{slug: nested_form_slug})

  defp put_nested_form_relationship(input, _type, _nested_form_slug), do: input

  defp put_nested_form_id(input, :table, nested_form_slug) when is_binary(nested_form_slug),
    do: Map.put(input, :row_form_id, nested_form_slug)

  defp put_nested_form_id(input, :form, nested_form_slug) when is_binary(nested_form_slug),
    do: Map.put(input, :sub_form_id, nested_form_slug)

  defp put_nested_form_id(input, _type, _nested_form_slug), do: input
end
