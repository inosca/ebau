import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | user", function (hooks) {
  setupTest(hooks);

  test("it computes the full name", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("user", {
      name: "Max",
      surname: "Muster",
    });

    assert.strictEqual(model.fullName, "Max Muster");
  });
});
