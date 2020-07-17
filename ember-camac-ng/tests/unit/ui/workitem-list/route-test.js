import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | workitem-list", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const route = this.owner.lookup("route:workitem-list");
    assert.ok(route);
  });
});
