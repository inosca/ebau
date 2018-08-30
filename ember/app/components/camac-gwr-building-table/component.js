import Component from "@ember/component";
import { task } from "ember-concurrency";
import v4 from "uuid/v4";

export default Component.extend({
  addRow: task(function*() {
    let row = {
      uuid: v4(),
      ...this.get("config.columns").reduce(
        (obj, { name }) => ({ ...obj, [name]: "" }),
        {}
      )
    };

    yield this.setProperties({
      editedRow: row,
      showEdit: true
    });
  }).drop(),

  saveRow: task(function*(row) {
    yield this.getWithDefault(
      "attrs.on-change",
      () => {}
    )([...this.getWithDefault("value", []).filter(r => r.uuid !== row.uuid), row]);

    this.setProperties({
      editedRow: null,
      showEdit: false
    });
  }).restartable(),

  editRow: task(function*(row) {
    yield this.setProperties({
      editedRow: row,
      showEdit: true
    });
  }).restartable(),

  deleteRow: task(function*(row) {
    yield this.getWithDefault(
      "attrs.on-change",
      () => {}
    )(this.getWithDefault("value", []).filter(r => r.uuid !== row.uuid));

    this.setProperties({
      editedRow: null,
      showEdit: false
    });
  })
});
