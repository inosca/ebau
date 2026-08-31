defmodule Ebau.Test.InstanceFixtures do
  @moduledoc """
  ExUnit setup callbacks for instance tests. Everything goes through the real
  domain actions:

      import Ebau.Test.InstanceFixtures

      setup [:create_workflow, :create_form, :create_instance]
  """

  @opts [authorize?: false, actor: nil]

  def create_workflow(_context) do
    Caluma.Test.Fixtures.create_workflow!("building-permit")
    :ok
  end

  @doc """
  Creates the `baugesuch` form with every answer and table question
  `Ebau.Instances.Instance` declares, under the slugs this build's canton
  resolves.
  """
  def create_form(_context) do
    Caluma.Test.Fixtures.create_form!("baugesuch", Ebau.Instances.Instance)
    :ok
  end

  def create_instance(_context), do: %{instance: create_instance!()}

  @doc """
  Creates an instance through `Ebau.Instances.create_instance!`, starting its
  case on the form. Params (e.g. `proposal: "Neubau"`) pass through.
  """
  def create_instance!(params \\ %{}) do
    Ebau.Instances.create_instance!(
      Map.merge(%{case: %{workflow: %{slug: "building-permit"}}}, Map.new(params)),
      @opts
    )
  end

  @doc "The id of the Caluma document behind `instance`'s case."
  def document_id!(instance) do
    Ash.load!(instance, :case, @opts).case.document_id
  end
end
