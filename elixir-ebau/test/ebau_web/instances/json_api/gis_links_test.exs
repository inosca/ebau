defmodule EbauWeb.Instances.GisLinksTest do
  use EbauWeb.ConnCase, async: true

  setup %{conn: conn} do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    Ebau.User.create_role!(%{slug: "municipality"}, authorize?: false, actor: nil)

    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    gis_link =
      Ebau.Instances.create_gis_link!(
        %{name: "My GIS link", placeholder: "https://example.com?x={x}&y={y}"},
        actor: actor
      )

    %{conn: authenticated_rest_api_conn(conn, actor), actor: actor, gis_link: gis_link}
  end

  describe "read_gis_links" do
    test "returns gis links for my service", %{conn: conn, gis_link: gis_link} do
      %{"data" => data} =
        conn
        |> get(~p"/api/v2/gis-links")
        |> json_response(200)

      assert Enum.map(data, & &1["id"]) == [gis_link.id]
    end

    test "does not return gis links for other services", %{conn: conn} do
      other_actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

      other_gis_link =
        Ebau.Instances.create_gis_link!(
          %{name: "Other GIS link", placeholder: "https://example.com?x={x}&y={y}"},
          actor: other_actor
        )

      %{"data" => data} =
        conn
        |> get(~p"/api/v2/gis-links")
        |> json_response(200)

      refute Enum.any?(data, &(&1["id"] == other_gis_link.id))
    end
  end

  describe "create_gis_link" do
    test "creates a gis link for municipality admins", %{conn: conn, actor: actor} do
      %{"data" => data} =
        conn
        |> put_req_header("content-type", "application/vnd.api+json")
        |> post(~p"/api/v2/gis-links", create_payload("Created", actor))
        |> json_response(201)

      assert data["type"] == "gis-links"
      assert data["attributes"]["name"] == "Created"
      assert data["attributes"]["placeholder"] == "https://example.com?x={x}&y={y}"

      %{"data" => gis_links} =
        conn
        |> get(~p"/api/v2/gis-links")
        |> json_response(200)

      assert Enum.any?(gis_links, &(&1["id"] == data["id"]))
    end

    test "forbids creating gis links for non-admins", %{conn: conn} do
      not_admin_actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality"}})

      conn =
        conn
        |> authenticated_rest_api_conn(not_admin_actor)
        |> post(~p"/api/v2/gis-links", create_payload("Blocked", not_admin_actor))

      assert json_response(conn, 403)
    end

    defp create_payload(name, actor) do
      %{
        data: %{
          type: "gis-links",
          attributes: %{
            name: name,
            placeholder: "https://example.com?x={x}&y={y}"
          },
          relationships: %{
            service: %{
              data: %{
                type: "services",
                id: Integer.to_string(actor.service.id)
              }
            }
          }
        }
      }
    end
  end

  describe "destroy_gis_link" do
    test "deletes a gis link for municipality admins", %{conn: conn, gis_link: gis_link} do
      conn
      |> delete(~p"/api/v2/gis-links/#{gis_link.id}")
      |> response(200)

      %{"data" => data} =
        conn
        |> get(~p"/api/v2/gis-links")
        |> json_response(200)

      refute Enum.any?(data, &(&1["id"] == gis_link.id))
    end

    test "forbids deleting gis links for non-admins", %{conn: conn, gis_link: gis_link} do
      not_admin_actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality"}})

      conn =
        conn
        |> authenticated_rest_api_conn(not_admin_actor)
        |> delete(~p"/api/v2/gis-links/#{gis_link.id}")

      assert json_response(conn, 403)
    end

    test "forbids deleting gis links for admins of other services", %{
      conn: conn,
      gis_link: gis_link
    } do
      other_admin = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

      conn =
        conn
        |> authenticated_rest_api_conn(other_admin)
        |> delete(~p"/api/v2/gis-links/#{gis_link.id}")

      # 404 because the read policy filters out links from other services
      assert json_response(conn, 404)
    end
  end
end
