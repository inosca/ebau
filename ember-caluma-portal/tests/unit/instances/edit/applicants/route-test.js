import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";

module("Unit | Route | instances/edit/applicants", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:instances/edit/applicants");
    assert.ok(route);
  });
});
