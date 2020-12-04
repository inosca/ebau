import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | instance", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:instance");
    assert.ok(ability);
  });
});
