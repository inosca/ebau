import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module(
  "Unit | Route | protected/cases/detail/communications/detail",
  function (hooks) {
    setupTest(hooks);

    test("it exists", function (assert) {
      const route = this.owner.lookup(
        "route:protected/cases/detail/communications/detail"
      );
      assert.ok(route);
    });
  }
);
