defmodule Caluma.Form do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Caluma.Form.Document
    resource Caluma.Form.Answer
    resource Caluma.Form.AnswerDocument
  end
end
