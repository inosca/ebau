defmodule Caluma.Form do
  @moduledoc """
  Ash domain for Caluma form resources (forms, questions, documents, answers).

  This is a partial Elixir clone of the Caluma form module. It reads from and
  writes to the same PostgreSQL tables that the upstream Django Caluma service
  manages. Only the subset of models needed by the eBau Elixir app is
  represented here.

  See https://github.com/projectcaluma/caluma for upstream documentation.
  """

  use Ash.Domain,
    otp_app: :ebau

  authorization do
    authorize :by_default
  end

  resources do
    resource Caluma.Form.Answer do
      define :create_answer, action: :create

      define :get_answer_by_document_and_question,
        action: :read,
        get_by: [:document_id, :question_id]
    end

    resource Caluma.Form.AnswerDocument

    resource Caluma.Form.Document do
      define :create_document
      define :create_row_document, args: [:document, :question, {:optional, :answers}]
    end

    resource Caluma.Form.Form do
      define :create_form
      define :create_form_tree
      define :apply_form_tree
      define :get_form_by_slug, action: :read, get_by: [:slug]
    end

    resource Caluma.Form.FormQuestion do
      define :create_form_question
      define :assert_form_question_compatible

      define :get_form_question_by_form_and_question,
        action: :read,
        get_by: [:form_id, :question_id]
    end

    resource Caluma.Form.Question do
      define :create_question
      define :assert_question_compatible
      define :get_question_by_slug, action: :read, get_by: [:slug]
    end
  end
end
