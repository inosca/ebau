import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | task-form", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:task-form");
    assert.ok(ability);
  });
});
