import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | work-item", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:work-item");
    assert.ok(ability);
  });
});
