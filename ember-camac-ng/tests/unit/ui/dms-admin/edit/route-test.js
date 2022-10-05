import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | dms-admin/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:dms-admin/edit");
    assert.ok(route);
  });
});
