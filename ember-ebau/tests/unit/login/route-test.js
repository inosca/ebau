import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Route | login", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:login");
    assert.ok(route);
  });
});
