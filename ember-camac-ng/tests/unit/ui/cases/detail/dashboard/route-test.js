import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | cases/detail/dashboard", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:cases/detail/dashboard");
    assert.ok(route);
  });
});
