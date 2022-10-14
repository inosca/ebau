import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | audit/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:audit/index");
    assert.ok(route);
  });
});
