import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Route | audit/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:audit/edit");
    assert.ok(route);
  });
});
