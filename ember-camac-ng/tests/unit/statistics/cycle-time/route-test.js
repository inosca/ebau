import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | statistics/cycle-time", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:statistics/cycle-time");
    assert.ok(route);
  });
});
