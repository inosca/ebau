import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | communications attachment", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("communications-attachment", {});
    assert.ok(model);
  });
});
