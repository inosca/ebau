import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module(
  "Unit | Route | protected/cases/detail/communications/index",
  function (hooks) {
    setupTest(hooks);

    test("it exists", function (assert) {
      const route = this.owner.lookup(
        "route:protected/cases/detail/communications/index"
      );
      assert.ok(route);
    });
  }
);
