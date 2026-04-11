defmodule Caluma.Form do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Caluma.Form.Answer do
      define :get_answer_by_document_and_question, action: :read, get_by: [:document, :question]
    end

    resource Caluma.Form.AnswerDocument

    resource Caluma.Form.Document do
      define :create_document
      define :create_row_document, args: [:document, :question, {:optional, :answers}]
    end

    resource Caluma.Form.Form do
      define :create_form
    end

    resource Caluma.Form.FormQuestion do
      define :create_form_question

      define :get_form_question_by_form_and_question,
        action: :read,
        get_by: [:form_id, :question_id]
    end

    resource Caluma.Form.Question do
      define :create_question
      define :get_question_by_slug, action: :read, get_by: [:slug]
    end
  end
end
