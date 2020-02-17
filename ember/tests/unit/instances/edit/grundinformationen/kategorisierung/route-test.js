import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module(
  "Unit | Route | instances/edit/grundinformationen/kategorisierung",
  function(hooks) {
    setupTest(hooks);

    test("it exists", function(assert) {
      const route = this.owner.lookup(
        "route:instances/edit/grundinformationen/kategorisierung"
      );
      assert.ok(route);
    });
  }
);
