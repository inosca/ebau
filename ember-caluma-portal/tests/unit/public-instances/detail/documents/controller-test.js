import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";

module(
  "Unit | Controller | public-instances/detail/documents",
  function (hooks) {
    setupTest(hooks);

    // TODO: Replace this with your real tests.
    test("it exists", function (assert) {
      const controller = this.owner.lookup(
        "controller:public-instances/detail/documents"
      );
      assert.ok(controller);
    });
  }
);
