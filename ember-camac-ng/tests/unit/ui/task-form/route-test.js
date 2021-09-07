import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | task-form", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:task-form");
    assert.ok(route);
  });
});
