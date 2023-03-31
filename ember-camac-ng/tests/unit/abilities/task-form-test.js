import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Ability | task-form", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:task-form");
    assert.ok(ability);
  });
});
