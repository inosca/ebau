import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | cases", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:cases");
    assert.ok(route);
  });
});
