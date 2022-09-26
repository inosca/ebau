import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Service | session", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:session");
    assert.ok(service);
  });
});
