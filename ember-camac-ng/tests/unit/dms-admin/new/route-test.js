import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | dms-admin/new", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:dms-admin/new");
    assert.ok(route);
  });
});
