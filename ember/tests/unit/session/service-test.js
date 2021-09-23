import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Service | session", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const service = this.owner.lookup("service:session");
    assert.ok(service);
  });
});
