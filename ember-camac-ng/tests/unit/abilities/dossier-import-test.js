import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

module("Unit | Ability | dossier-import", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:dossier-import");
    assert.ok(ability);
  });
});
