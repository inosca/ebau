defmodule Ebau.MasterData.PlotDataRowCrudTest do
  use Ebau.DataCase, async: true

  import Ebau.Test.InstanceFixtures

  setup [:create_workflow, :create_form, :create_instance]

  defp rows(instance) do
    Ash.load!(instance, [plot_data: [:coord_east, :coord_north, :plot_number]],
      authorize?: false,
      actor: nil
    ).plot_data
  end

  test "create makes a row readable through the instance", %{instance: instance} do
    Ebau.MasterData.create_plot_data_row!(
      %{
        document_id: document_id!(instance),
        coord_east: "1.0",
        coord_north: "2.0",
        plot_number: "12"
      },
      authorize?: false,
      actor: nil
    )

    assert [row] = rows(instance)
    assert row.coord_east == "1.0"
    assert row.coord_north == "2.0"
    assert row.plot_number == "12"
  end

  test "create adds one row per call", %{instance: instance} do
    for east <- ["1.0", "2.0"] do
      Ebau.MasterData.create_plot_data_row!(
        %{document_id: document_id!(instance), coord_east: east},
        authorize?: false,
        actor: nil
      )
    end

    assert rows(instance) |> Enum.map(& &1.coord_east) |> Enum.sort() == ["1.0", "2.0"]
  end

  test "update overwrites provided answers, keeps the rest", %{instance: instance} do
    row =
      Ebau.MasterData.create_plot_data_row!(
        %{document_id: document_id!(instance), coord_east: "1.0", plot_number: "12"},
        authorize?: false,
        actor: nil
      )

    Ebau.MasterData.update_plot_data_row!(row, %{coord_east: "9.0"},
      authorize?: false,
      actor: nil
    )

    assert [updated] = rows(instance)
    assert updated.coord_east == "9.0"
    assert updated.plot_number == "12"
  end

  test "update can set an answer the row did not have yet", %{instance: instance} do
    row =
      Ebau.MasterData.create_plot_data_row!(
        %{document_id: document_id!(instance), coord_east: "1.0"},
        authorize?: false,
        actor: nil
      )

    Ebau.MasterData.update_plot_data_row!(row, %{coord_north: "5.0"},
      authorize?: false,
      actor: nil
    )

    assert [%{coord_east: "1.0", coord_north: "5.0"}] = rows(instance)
  end

  test "destroy removes the row and its answers", %{instance: instance} do
    row =
      Ebau.MasterData.create_plot_data_row!(
        %{document_id: document_id!(instance), coord_east: "1.0"},
        authorize?: false,
        actor: nil
      )

    Ebau.MasterData.destroy_plot_data_row!(row, authorize?: false, actor: nil)

    assert rows(instance) == []

    assert Caluma.Form.list_answers_by_document!(row.id, authorize?: false, actor: nil) == []
  end
end
