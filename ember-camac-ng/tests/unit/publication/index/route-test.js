import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Route | publication/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:publication/index");
    assert.ok(route);
  });
});
