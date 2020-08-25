import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | work-items", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const route = this.owner.lookup("route:work-items");
    assert.ok(route);
  });
});
