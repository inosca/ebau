import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Service | material-exam-switcher", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:material-exam-switcher");
    assert.ok(service);
  });
});
