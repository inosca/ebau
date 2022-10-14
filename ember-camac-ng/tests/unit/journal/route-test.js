import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | journal", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:journal");
    assert.ok(route);
  });
});
