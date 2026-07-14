defmodule Ebau.Instances.Calculations.GisLinkForInstanceTest do
  use Ebau.DataCase, async: true

  import Ebau.Test.InstanceFixtures

  @geometry %{
    "markers" => [%{"x" => 2_760_907.75, "y" => 1_191_927.88}],
    "geometry" => "POINT",
    "center" => %{"x" => 2_760_907.75, "y" => 1_191_927.88}
  }

  setup [:create_workflow, :create_form]

  setup do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)

    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    gis_link =
      Ebau.Instances.create_gis_link!(
        %{name: "test", placeholder: "https://map.geo.admin.ch?center=999%2C999"},
        actor: actor
      )

    %{actor: actor, gis_link: gis_link}
  end

  test "replaces coordinate placeholders with the plot's coordinates", %{
    actor: actor,
    gis_link: gis_link
  } do
    instance = instance_with(plots: [%{east: "456.0", north: "123.0"}])

    assert link_for(gis_link, instance, actor) == "https://map.geo.admin.ch?center=456.0%2C123.0"
  end

  test "uses coordinates from the first plot when multiple exist", %{
    actor: actor,
    gis_link: gis_link
  } do
    instance =
      instance_with(plots: [%{east: "456.0", north: "123.0"}, %{east: "888.0", north: "999.0"}])

    assert link_for(gis_link, instance, actor) == "https://map.geo.admin.ch?center=456.0%2C123.0"
  end

  test "prefers the drawn geometry over the plot's coordinates", %{
    actor: actor,
    gis_link: gis_link
  } do
    instance =
      instance_with(geometry: @geometry, plots: [%{east: "456.0", north: "123.0"}])

    assert link_for(gis_link, instance, actor) ==
             "https://map.geo.admin.ch?center=2760907.75%2C1191927.88"
  end

  test "returns the placeholder if instance has no coordinates", %{
    actor: actor,
    gis_link: gis_link
  } do
    instance = instance_with([])

    assert link_for(gis_link, instance, actor) == "https://map.geo.admin.ch?center=999%2C999"
  end

  test "returns the placeholder if the first plot row has no coordinates", %{
    actor: actor,
    gis_link: gis_link
  } do
    instance = instance_with(plots: [%{}])

    assert link_for(gis_link, instance, actor) == "https://map.geo.admin.ch?center=999%2C999"
  end

  test "denies access to gis links for instances without an ACL", %{
    actor: actor,
    gis_link: gis_link
  } do
    instance = instance_with(plots: [%{east: "456.0", north: "123.0"}])

    assert_raise Ash.Error.Invalid, fn ->
      Ash.load!(gis_link, [gis_link_for_instance: %{instance_id: instance.id}], actor: actor)
    end
  end

  defp link_for(gis_link, instance, actor) do
    Ebau.Permissions.grant_acl_for_instance!(
      %{instance: %{id: instance.id}, user: %{id: actor.user.id}},
      authorize?: false,
      actor: nil
    )

    gis_link
    |> Ash.load!([gis_link_for_instance: %{instance_id: instance.id}], actor: actor)
    |> Map.fetch!(:gis_link_for_instance)
  end

  defp instance_with(opts) do
    instance =
      create_instance!(gis_map_geometry_json: opts[:geometry] && JSON.encode!(opts[:geometry]))

    Enum.each(opts[:plots] || [], fn plot ->
      Ebau.MasterData.create_plot_data_row!(
        %{
          document_id: document_id!(instance),
          coord_east: plot[:east],
          coord_north: plot[:north]
        },
        authorize?: false,
        actor: nil
      )
    end)

    instance
  end
end
