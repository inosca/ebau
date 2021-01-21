import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | dashboard", function (hooks) {
  setupTest(hooks);

  test("computes edit permission", function (assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:dashboard");

    ability.set("session", { isSupport: true });
    assert.ok(ability.canEdit);

    ability.set("session", { isSupport: false });
    assert.notOk(ability.canEdit);
  });
});
