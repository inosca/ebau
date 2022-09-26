import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Controller | support", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:support");
    assert.ok(controller);
  });
});
