import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";

module("Unit | Controller | instances/edit", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:instances/edit");
    assert.ok(controller);
  });
});
