import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | dms-template", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:dms-template");
    assert.ok(ability);
  });
});
