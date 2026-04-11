defmodule Ebau.Test.CantonFixtures do
  @moduledoc false

  alias Ebau.Legacy.ConfigLoader

  def load_canton_config!(canton) do
    ConfigLoader.load_application_config!("kt_#{canton}")
  end

  def load_canton_fixtures!(canton) do
    ConfigLoader.load_application_config!("kt_#{canton}", scope: :all)
  end

  def canton_files!(canton, scope \\ :config) do
    ConfigLoader.application_files!("kt_#{canton}", scope)
  end

  def supported_models do
    ConfigLoader.supported_models()
  end

  def load_files!(paths) do
    ConfigLoader.load_files!(paths)
  end
end
