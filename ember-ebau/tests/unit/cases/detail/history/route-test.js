import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Route | cases/detail/history", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:cases/detail/history");
    assert.ok(route);
  });
});
