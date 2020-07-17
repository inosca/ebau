import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module(
  "Unit | Route | instances/edit/baumeldung-fur-geringfugige-vorhaben",
  function (hooks) {
    setupTest(hooks);

    test("it exists", function (assert) {
      const route = this.owner.lookup(
        "route:instances/edit/baumeldung-fur-geringfugige-vorhaben"
      );
      assert.ok(route);
    });
  }
);
