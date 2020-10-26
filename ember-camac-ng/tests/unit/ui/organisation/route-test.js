import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | organisation", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:organisation");
    assert.ok(route);
  });
});
