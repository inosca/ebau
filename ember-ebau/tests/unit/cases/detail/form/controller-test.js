import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Controller | cases/detail/form", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:cases/detail/form");
    assert.ok(controller);
  });
});
