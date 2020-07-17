import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

import config from "../../../config/environment";

module("Unit | Ability | dashboard", function (hooks) {
  setupTest(hooks);

  test("computes edit permission", function (assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:dashboard");

    ability.set("session", { group: config.ebau.supportGroups[0] });
    assert.ok(ability.canEdit);

    ability.set("session", { group: 123 });
    assert.notOk(ability.canEdit);
  });
});
