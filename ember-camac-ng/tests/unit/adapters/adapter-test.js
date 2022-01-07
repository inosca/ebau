import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | dossier import", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:dossier-import");
    assert.ok(adapter);
  });
});
