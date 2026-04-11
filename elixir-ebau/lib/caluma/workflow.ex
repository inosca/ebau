defmodule Caluma.Workflow do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Caluma.Workflow.Case do
      define :create_case
    end

    resource Caluma.Workflow.Workflow do
      define :create_workflow, action: :create
    end
  end
end
