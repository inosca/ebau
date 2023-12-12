import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | static content", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("static-content", {});
    assert.ok(model);
  });
});
