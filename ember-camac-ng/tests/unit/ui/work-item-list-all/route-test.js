import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | work-item-list-all", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const route = this.owner.lookup("route:work-item-list-all");
    assert.ok(route);
  });
});
