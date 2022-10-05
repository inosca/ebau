import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | dms-admin/index", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:dms-admin/index");
    assert.ok(controller);
  });
});
