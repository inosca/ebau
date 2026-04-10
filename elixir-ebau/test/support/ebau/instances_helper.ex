defmodule Ebau.Test.InstancesHelper do
  def create_instance! do
    Ebau.Instances.create_instance!(authorize?: false)
  end
end
