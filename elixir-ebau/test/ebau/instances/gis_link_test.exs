defmodule Ebau.Instances.GisLinkTest do
  use Ebau.DataCase, async: true

  alias Ebau.Instances.GisLink

  describe "supported_providers/0" do
    test "offers the federal map to every canton" do
      assert %{"center" => center} = GisLink.supported_providers()["map.geo.admin.ch"]
      assert center.("456", "123") == "456,123"
    end

    @tag canton: :gr
    test "offers the three GR maps and no foreign canton's map" do
      assert GisLink.supported_providers() |> Map.keys() |> Enum.sort() == [
               "geo-surselva.ch",
               "map.geo.admin.ch",
               "map.geo.gr.ch",
               "poschiavo.mapplus.ch"
             ]
    end

    @tag canton: :gr
    test "maps east and north to the separate parameters the GR maps expect" do
      providers = GisLink.supported_providers()

      for host <- ["map.geo.gr.ch", "poschiavo.mapplus.ch", "geo-surselva.ch"] do
        [{east_param, east_fun}, {north_param, north_fun}] =
          providers |> Map.fetch!(host) |> Enum.sort()

        assert east_fun.("456", "123") == "456"
        assert north_fun.("456", "123") == "123"
        assert String.ends_with?(east_param, "x")
        assert String.ends_with?(north_param, "y")
      end
    end

    @tag canton: :so
    test "offers the SO map, which takes both coordinates in one parameter" do
      assert GisLink.supported_providers() |> Map.keys() |> Enum.sort() == [
               "geo.so.ch",
               "map.geo.admin.ch"
             ]

      assert %{"c" => c} = GisLink.supported_providers()["geo.so.ch"]
      assert c.("456", "123") == "456,123"
    end

    @tag canton: :sg
    test "offers the SG maps, which expect east and north swapped" do
      providers = GisLink.supported_providers()

      assert providers |> Map.keys() |> Enum.sort() == [
               "geoportal.ch",
               "map.geo.admin.ch",
               "oereb.geo.sg.ch"
             ]

      for host <- ["geoportal.ch", "oereb.geo.sg.ch"] do
        assert %{"x" => x_fun, "y" => y_fun} = Map.fetch!(providers, host)

        # returns y, not x
        assert x_fun.("456", "123") == "123"
        # returns x, not y
        assert y_fun.("456", "123") == "456"
      end
    end
  end

  describe "provider_for_host/1" do
    test "ignores casing and a www prefix" do
      assert GisLink.provider_for_host("map.geo.admin.ch")
      assert GisLink.provider_for_host("www.map.geo.admin.ch")
      assert GisLink.provider_for_host("MAP.GEO.ADMIN.CH")
    end

    test "returns nil for an unknown host and for nil" do
      refute GisLink.provider_for_host("example.com")
      refute GisLink.provider_for_host(nil)
    end
  end

  describe "creating a gis link" do
    setup do
      Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)

      %{actor: Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})}
    end

    test "accepts a placeholder on a supported provider", %{actor: actor} do
      assert {:ok, gis_link} =
               Ebau.Instances.create_gis_link(
                 %{name: "test", placeholder: "https://map.geo.admin.ch?center=0,0"},
                 actor: actor
               )

      assert gis_link.placeholder == "https://map.geo.admin.ch?center=0,0"
    end

    test "accepts a placeholder on a www-prefixed provider", %{actor: actor} do
      placeholder = "https://www.map.geo.admin.ch?center=0,0"

      assert {:ok, gis_link} =
               Ebau.Instances.create_gis_link(
                 %{name: "test", placeholder: placeholder},
                 actor: actor
               )

      assert gis_link.placeholder == placeholder
    end

    test "rejects a placeholder on an unknown provider", %{actor: actor} do
      assert {:error, error} =
               Ebau.Instances.create_gis_link(
                 %{name: "test", placeholder: "https://example.com?center=0,0"},
                 actor: actor
               )

      assert Exception.message(error) =~ "Invalid GIS provider"
    end

    @tag canton: :gr
    test "rejects another canton's provider", %{actor: actor} do
      assert {:error, error} =
               Ebau.Instances.create_gis_link(
                 %{name: "test", placeholder: "https://geo.so.ch?c=0,0"},
                 actor: actor
               )

      assert Exception.message(error) =~ "Invalid GIS provider"
    end
  end
end
