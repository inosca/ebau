import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | statistics/process-time", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:statistics/process-time");
    assert.ok(route);
  });
});
