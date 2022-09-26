import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Service | notifications", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:notification");
    assert.ok(service);
  });
});
