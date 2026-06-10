defmodule Caluma.Form.AnswerFilters do
  @moduledoc false

  require Ash.Expr

  @doc """
  Filter for a `has_one :answer` relationship on a Caluma document parent.
  Selects the single answer matching one of `slugs` on the parent document
  identified by `parent_doc_id_ref` (an `%Ash.Query.Ref{}`). This is split
  up into two implementations for performance reasons as `question_id ==`
  is more efficient on big data sets than `question_id in`.
  """
  def answer_filter(parent_doc_id_ref, {_mod, opts}) do
    # TODO: eval the canton_resolver at run time with context
    answer_filter(
      parent_doc_id_ref,
      opts[:default]
    )
  end

  def answer_filter(parent_doc_id_ref, slug) when is_binary(slug),
    do: answer_filter(parent_doc_id_ref, [slug])

  def answer_filter(parent_doc_id_ref, [single_slug]),
    do: Ash.Expr.expr(document_id == parent(^parent_doc_id_ref) and question_id == ^single_slug)

  def answer_filter(parent_doc_id_ref, slugs),
    do: Ash.Expr.expr(document_id == parent(^parent_doc_id_ref) and question_id in ^slugs)

  @doc """
  Filter for a `has_many` relationship to row documents under a table question.
  Selects all row documents in the parent's family for one of `slugs`. Parent
  document is identified by `parent_doc_id_ref` (an `%Ash.Query.Ref{}`).
  This is split up into two implementations for performance reasons as
  `question_id ==` is more efficient on big data sets than `question_id in`.
  """
  def table_filter(parent_doc_id_ref, {_mod, opts}) when is_map(opts) do
    # TODO: eval the canton_resolver at run time with context
    table_filter(parent_doc_id_ref, opts[:default])
  end

  def table_filter(parent_doc_id_ref, single_slug) when is_binary(single_slug),
    do: table_filter(parent_doc_id_ref, [single_slug])

  def table_filter(parent_doc_id_ref, [single_slug]) do
    Ash.Expr.expr(
      family.id == parent(^parent_doc_id_ref) and
        exists(answer_documents, answer.question_id == ^single_slug)
    )
  end

  def table_filter(parent_doc_id_ref, slugs) do
    Ash.Expr.expr(
      family.id == parent(^parent_doc_id_ref) and
        exists(answer_documents, answer.question_id in ^slugs)
    )
  end
end
