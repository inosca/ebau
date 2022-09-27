import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | cases/detail/work-items/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:cases/detail/work-items/edit");
    assert.ok(route);
  });
});
