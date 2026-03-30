defmodule Caluma.Workflow do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Caluma.Workflow.Case
  end
end
