import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | dossier-import/new", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:dossier-import/new");
    assert.ok(controller);
  });
});
