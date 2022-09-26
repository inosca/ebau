import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Route | statistics/avg-cycle-time", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:statistics/avg-cycle-time");
    assert.ok(route);
  });
});
