defmodule Caluma.Workflow do
  @moduledoc """
  Ash domain for Caluma workflow resources (workflows, cases).

  This is a partial Elixir clone of the Caluma workflow module. It reads from
  and writes to the same PostgreSQL tables that the upstream Django Caluma
  service manages. Only the subset of models needed by the eBau Elixir app is
  represented here.

  See https://github.com/projectcaluma/caluma for upstream documentation.
  """

  use Ash.Domain,
    otp_app: :ebau

  authorization do
    authorize :by_default
  end

  resources do
    resource Caluma.Workflow.Case do
      define :create_case
    end

    resource Caluma.Workflow.Workflow do
      define :create_workflow, action: :create
    end
  end
end
