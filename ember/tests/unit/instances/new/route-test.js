import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Route | instances/new", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    let route = this.owner.lookup("route:instances/new");
    assert.ok(route);
  });
});
