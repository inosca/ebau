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

    resource Caluma.Form.FormQuestion

    resource Caluma.Form.Question do
      define :get_question_by_slug, action: :read, get_by: [:slug]
    end
  end
end
