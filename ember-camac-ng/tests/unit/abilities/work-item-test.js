import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Ability | work-item", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:work-item");
    assert.ok(ability);
  });
});
