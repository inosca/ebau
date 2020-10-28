import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | history entry", function (hooks) {
  setupTest(hooks);

  test("it computes the correct icon for the type", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("history-entry", {});

    assert.equal(model.icon, null);

    model.set("historyType", "notification");
    assert.equal(model.icon, "envelope");

    model.set("historyType", "status-change");
    assert.equal(model.icon, "check-circle");
  });
});
