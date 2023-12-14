import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Ability | message", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:message");
    assert.ok(ability);
  });
});
