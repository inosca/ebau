import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Adapter | instance", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:instance");
    assert.ok(adapter);
  });
});
