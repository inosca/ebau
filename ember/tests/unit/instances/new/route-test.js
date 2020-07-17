import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | instances/new", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:instances/new");
    assert.ok(route);
  });
});
