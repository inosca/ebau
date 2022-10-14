import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | cases/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:cases/index");
    assert.ok(route);
  });
});
