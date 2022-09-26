import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Route | protected", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:protected");
    assert.ok(route);
  });
});
