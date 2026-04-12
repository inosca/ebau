defmodule Ebau.Instances.Calculations.GisLinksForInstanceTest do
  use Ebau.DataCase, async: true

  setup do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false)
    Caluma.Workflow.create_workflow!(%{slug: "building-permit", name: %{"de" => "workflow"}})
    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})
    case = Caluma.Workflow.create_case!(%{workflow: %{slug: "building-permit"}})
    instance = Ebau.Instances.create_instance!(%{case: %{id: case.id}}, authorize?: false)
    doc = Ebau.Test.GisLinkHelper.create_caluma_form_and_document(case)

    gis_link =
      Ebau.Instances.create_gis_link!(
        %{name: "test", placeholder: "https://example.com?x={x}&y={y}"},
        actor: actor
      )

    %{
      actor: actor,
      instance: instance,
      gis_link: gis_link,
      doc: doc
    }
  end

  test "replaces coordinate placeholders with first plot's coordinates", %{
    actor: actor,
    instance: instance,
    gis_link: gis_link
  } do
    Ebau.Permissions.grant_acl_for_instance!(
      %{instance: %{id: instance.id}, user: %{id: actor.user.id}},
      authorize?: false
    )

    gis_link =
      Ash.load!(gis_link, [gis_link_for_instance: %{instance_id: instance.id}], actor: actor)

    assert gis_link.gis_link_for_instance == "https://example.com?x=456&y=123"
  end

  test "uses coordinates from the first plot when multiple exist", %{
    actor: actor,
    instance: instance,
    gis_link: gis_link,
    doc: doc
  } do
    Caluma.Form.create_row_document!(doc, %{slug: "parzellen"}, [
      %{question_id: "lagekoordinaten-nord", value: 999},
      %{question_id: "lagekoordinaten-ost", value: 888}
    ])

    Ebau.Permissions.grant_acl_for_instance!(
      %{instance: %{id: instance.id}, user: %{id: actor.user.id}},
      authorize?: false
    )

    gis_link =
      Ash.load!(gis_link, [gis_link_for_instance: %{instance_id: instance.id}], actor: actor)

    assert gis_link.gis_link_for_instance == "https://example.com?x=456&y=123"
  end

  test "returns empty coordinates when instance has no plot data", %{
    actor: actor,
    gis_link: gis_link
  } do
    empty_case = Caluma.Workflow.create_case!(%{workflow: %{slug: "building-permit"}})

    empty_instance =
      Ebau.Instances.create_instance!(%{case: %{id: empty_case.id}}, authorize?: false)

    Ebau.Permissions.grant_acl_for_instance!(
      %{instance: %{id: empty_instance.id}, user: %{id: actor.user.id}},
      authorize?: false
    )

    gis_link =
      Ash.load!(
        gis_link,
        [gis_link_for_instance: %{instance_id: empty_instance.id}],
        actor: actor
      )

    assert gis_link.gis_link_for_instance == "https://example.com?x=&y="
  end

  test "denies access to gis links for instances without an ACL", %{
    actor: actor,
    instance: instance,
    gis_link: gis_link
  } do
    assert_raise Ash.Error.Invalid, fn ->
      Ash.load!(gis_link, [gis_link_for_instance: %{instance_id: instance.id}], actor: actor)
    end
  end
end
