import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Route | cases/detail/work-items", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    let route = this.owner.lookup("route:cases/detail/work-items");
    assert.ok(route);
  });
});
