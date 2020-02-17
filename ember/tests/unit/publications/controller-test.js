import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | publications", function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function(assert) {
    const controller = this.owner.lookup("controller:publications");
    assert.ok(controller);
  });
});
