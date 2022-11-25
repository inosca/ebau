import { setupTest } from "dummy/tests/helpers";
import { module, test } from "qunit";

module("Unit | Model | communication communications-entity", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("communications-entity", {});
    assert.ok(model);
  });
});
