import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | statistics/avg-cycle-time", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:statistics/avg-cycle-time");
    assert.ok(route);
  });
});
