import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | task-form", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:task-form");
    assert.ok(controller);
  });
});
