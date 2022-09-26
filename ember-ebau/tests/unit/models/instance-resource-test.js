import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Model | instance resource", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("instance-resource", {});
    assert.ok(model);
  });
});
