import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | instance acl", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("instance-acl", {});
    assert.ok(model);
  });
});
