import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Controller | cases/index", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:cases/index");
    assert.ok(controller);
  });
});
