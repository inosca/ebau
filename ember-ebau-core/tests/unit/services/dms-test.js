import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Service | dms", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:dms");
    assert.ok(service);
  });
});
