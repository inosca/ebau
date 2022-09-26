import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Route | form", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:form");
    assert.ok(route);
  });
});
