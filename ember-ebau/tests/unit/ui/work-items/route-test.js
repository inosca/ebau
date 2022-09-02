import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Route | work-items", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    let route = this.owner.lookup("route:work-items");
    assert.ok(route);
  });
});
