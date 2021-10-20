import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { restartableTask, dropTask } from "ember-concurrency-decorators";
import { v4 } from "uuid";

export default class CamacGwrBuildingTableComponent extends Component {
  @tracked editedRow;
  @tracked showEdit;

  @action
  addRow() {
    const row = {
      uuid: v4(),
      ...this.args.config.columns.reduce(
        (obj, { name }) => ({ ...obj, [name]: "" }),
        {}
      ),
    };

    this.editedRow = row;
    this.showEdit = true;
  }

  @restartableTask
  *saveRow(row) {
    yield (this.args.onChange ?? (() => {}))([
      ...(this.args.value ?? []).filter((r) => r.uuid !== row.uuid),
      row,
    ]);

    this.editedRow = null;
    this.showEdit = false;
  }

  @action
  editRow(row) {
    this.editedRow = row;
    this.showEdit = true;
  }

  @dropTask
  *deleteRow(row) {
    yield (this.args.onChange ?? (() => {}))(
      (this.args.value ?? []).filter((r) => r.uuid !== row.uuid)
    );

    this.editedRow = null;
    this.showEdit = false;
  }
}
