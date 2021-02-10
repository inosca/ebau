import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | publication/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:publication/index");
    assert.ok(route);
  });
});
