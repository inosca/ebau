import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | support", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:support");
    assert.ok(route);
  });
});
