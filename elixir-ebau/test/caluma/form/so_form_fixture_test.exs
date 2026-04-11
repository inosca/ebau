defmodule Caluma.Form.SOFormFixtureTest do
  use Ebau.DataCase, async: false

  alias Caluma.Form.Document
  alias Ebau.Test.CantonFixtures

  @moduletag canton: :so

  setup tags do
    CantonFixtures.load_canton_config!(tags.canton)
    :ok
  end

  test "loads SO baugesuch form and creates a document from it" do
    assert form_exists?("baugesuch")

    document = Caluma.Form.create_document!(%{form: %{slug: "baugesuch"}})

    loaded_document = Ash.load!(document, [:form])

    assert document.form_id == "baugesuch"
    assert loaded_document.form.slug == "baugesuch"
    assert %Document{} = document
  end

  defp form_exists?(slug) do
    %{rows: [[count]]} =
      Ecto.Adapters.SQL.query!(
        Repo,
        "select count(*) from caluma_form_form where slug = $1",
        [slug]
      )

    count == 1
  end
end
