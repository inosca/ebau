defmodule Caluma.Form.AnswerFilters do
  @moduledoc false

  require Ash.Expr

  @doc """
  Filter for a `has_one :answer` relationship on a Caluma document parent.
  Selects the single answer matching one of `slugs` on the parent document
  identified by `parent_doc_id_ref` (an `%Ash.Query.Ref{}`).
  """
  def answer_filter(parent_doc_id_ref, [single_slug]),
    do: Ash.Expr.expr(document_id == parent(^parent_doc_id_ref) and question_id == ^single_slug)

  def answer_filter(parent_doc_id_ref, slugs),
    do: Ash.Expr.expr(document_id == parent(^parent_doc_id_ref) and question_id in ^slugs)

  @doc """
  Filter for a `has_many` relationship to row documents under a table question.
  Selects all row documents in the parent's family for one of `slugs`. Parent
  document is identified by `parent_doc_id_ref` (an `%Ash.Query.Ref{}`).
  """
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
