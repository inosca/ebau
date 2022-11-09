import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | publication/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:publication/edit");
    assert.ok(route);
  });
});
