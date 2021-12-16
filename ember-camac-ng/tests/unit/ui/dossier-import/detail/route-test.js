import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | dossier-import/detail", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:dossier-import/detail");
    assert.ok(route);
  });
});
