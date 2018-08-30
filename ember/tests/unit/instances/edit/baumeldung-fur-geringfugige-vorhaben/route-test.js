import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module(
  "Unit | Route | instances/edit/baumeldung-fur-geringfugige-vorhaben",
  function(hooks) {
    setupTest(hooks);

    test("it exists", function(assert) {
      let route = this.owner.lookup(
        "route:instances/edit/baumeldung-fur-geringfugige-vorhaben"
      );
      assert.ok(route);
    });
  }
);
