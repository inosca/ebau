import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | work-items.instance", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:work-items.instance");
    assert.ok(route);
  });
});
