import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Controller | form", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:form");
    assert.ok(controller);
  });
});
