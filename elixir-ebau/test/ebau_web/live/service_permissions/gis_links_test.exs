defmodule EbauWeb.Live.ServicePermissions.GisLinksTest do
  use EbauWeb.ConnCase, async: true

  setup %{conn: conn} do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)

    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    gis_link =
      Ebau.Instances.create_gis_link!(
        %{name: "My GIS link", placeholder: "https://map.geo.admin.ch"},
        actor: actor
      )

    %{conn: log_in_actor(conn, actor), actor: actor, gis_link: gis_link}
  end

  describe "mount" do
    test "renders existing gis links for the actor's service", %{conn: conn, gis_link: gis_link} do
      conn
      |> visit(~p"/service-permissions/gis-links")
      |> assert_has("td", text: gis_link.name)
      |> assert_has("td", text: gis_link.placeholder)
    end

    test "does not render gis links from other services", %{conn: conn} do
      other_actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

      other_link =
        Ebau.Instances.create_gis_link!(
          %{name: "Other service link", placeholder: "https://map.geo.admin.ch?center=0,0"},
          actor: other_actor
        )

      conn
      |> visit(~p"/service-permissions/gis-links")
      |> refute_has("td", text: other_link.name)
    end
  end

  describe "create" do
    test "creates a gis link on valid submit", %{conn: conn} do
      conn
      |> visit(~p"/service-permissions/gis-links")
      |> within("#new-gis-link", fn session ->
        session
        |> fill_in("Name", with: "Second", exact: false)
        |> fill_in("Link", with: "https://map.geo.admin.ch/map", exact: false)
        |> submit()
      end)
      |> assert_has("td", text: "Second")
      |> assert_has("td", text: "https://map.geo.admin.ch/map")
    end
  end

  describe "search" do
    test "filters the stream by matching name", %{conn: conn, actor: actor, gis_link: gis_link} do
      other =
        Ebau.Instances.create_gis_link!(
          %{name: "Parcels map", placeholder: "https://map.geo.admin.ch?center=0,0"},
          actor: actor
        )

      conn
      |> visit(~p"/service-permissions/gis-links")
      |> fill_in("Suche", with: "Parcels", exact: false)
      |> assert_has("td", text: other.name)
      |> refute_has("td", text: gis_link.name)
    end

    test "clearing the search restores the full list", %{
      conn: conn,
      actor: actor,
      gis_link: gis_link
    } do
      other =
        Ebau.Instances.create_gis_link!(
          %{name: "Parcels map", placeholder: "https://map.geo.admin.ch?center=0,0"},
          actor: actor
        )

      conn
      |> visit(~p"/service-permissions/gis-links")
      |> fill_in("Suche", with: "Parcels", exact: false)
      |> refute_has("td", text: gis_link.name)
      |> fill_in("Suche", with: "", exact: false)
      |> assert_has("td", text: gis_link.name)
      |> assert_has("td", text: other.name)
    end
  end

  describe "delete" do
    test "removes the gis link from the stream", %{conn: conn, gis_link: gis_link} do
      conn
      |> visit(~p"/service-permissions/gis-links")
      |> assert_has("td", text: gis_link.name)
      |> click_button("Löschen")
      |> refute_has("td", text: gis_link.name)
    end
  end
end
