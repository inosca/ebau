import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | dms-generate", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:dms-generate");
    assert.ok(route);
  });
});
