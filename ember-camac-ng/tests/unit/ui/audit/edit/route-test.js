import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | audit/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:audit/edit");
    assert.ok(route);
  });
});
