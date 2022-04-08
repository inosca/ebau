import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Controller | cases/detail/work-items/new", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    let controller = this.owner.lookup(
      "controller:cases/detail/work-items/new"
    );
    assert.ok(controller);
  });
});
