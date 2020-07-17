import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | notfound", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:notfound");
    assert.ok(route);
  });
});
