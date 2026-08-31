defmodule Caluma.Test.Domain do
  @moduledoc """
  Generic Caluma test resources: `Caluma.Test.Document`, a root document with
  answers and a `rows` table, and `Caluma.Test.Row`, its row resource. Use
  them to test Caluma changes and extensions without canton resources.
  """

  use Ash.Domain, validate_config_inclusion?: false

  resources do
    resource Caluma.Test.Document do
      define :create_document, action: :create
      define :update_document, action: :update
    end

    resource Caluma.Test.Row do
      define :create_row, action: :create
      define :update_row, action: :update
      define :destroy_row, action: :destroy
    end
  end
end
