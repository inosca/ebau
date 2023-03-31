import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Adapter | template", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:template");
    assert.ok(adapter);
  });
});
