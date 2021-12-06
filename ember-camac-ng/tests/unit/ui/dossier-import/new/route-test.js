import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | dossier-import/new", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:dossier-import/new");
    assert.ok(route);
  });
});
