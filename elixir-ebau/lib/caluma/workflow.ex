defmodule Caluma.Workflow do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Caluma.Workflow.Case do
      define :create_case
    end

    resource Caluma.Workflow.Workflow
  end
end
