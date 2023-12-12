import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Ability | topic", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:topic");
    assert.ok(ability);
  });
});
