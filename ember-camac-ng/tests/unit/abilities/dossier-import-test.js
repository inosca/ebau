import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | dossier-import", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:dossier-import");
    assert.ok(ability);
  });
});
