import { module, test } from "qunit";

import { setupTest } from "ebau/tests/helpers";

module("Unit | Route | cases/detail/work-items/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:cases/detail/work-items/edit");
    assert.ok(route);
  });
});
