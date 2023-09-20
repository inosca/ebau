import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";

module("Unit | Ability | dashboard", function (hooks) {
  setupTest(hooks);

  test("computes edit permission", async function (assert) {
    const ability = this.owner.lookup("ability:dashboard");

    ability.set("session", { isSupport: true });
    assert.ok(ability.canEdit);

    ability.set("session", { isSupport: false });
    assert.notOk(ability.canEdit);
  });
});
