import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Route | work-items", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:work-items");
    assert.ok(route);
  });
});
