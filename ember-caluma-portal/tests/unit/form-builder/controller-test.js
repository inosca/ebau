import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";

module("Unit | Controller | form-builder", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:form-builder");
    assert.ok(controller);
  });
});
