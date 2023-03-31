import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Service | gwr-data-import", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:gwr-data-import");
    assert.ok(service);
  });
});
