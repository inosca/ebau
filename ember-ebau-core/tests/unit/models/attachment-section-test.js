import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | attachment section", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("attachment-section", {});
    assert.ok(model);
  });
});
