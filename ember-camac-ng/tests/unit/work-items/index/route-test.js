import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | work-items.index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:work-items.index");
    assert.ok(route);
  });
});
