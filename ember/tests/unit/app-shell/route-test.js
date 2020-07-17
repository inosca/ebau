import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | app-shell", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:app-shell");
    assert.ok(route);
  });
});
