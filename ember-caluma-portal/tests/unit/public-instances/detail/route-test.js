import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | public-instances/detail", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:public-instances/detail");
    assert.ok(route);
  });
});
