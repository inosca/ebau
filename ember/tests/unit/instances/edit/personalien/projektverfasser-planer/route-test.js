import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module(
  "Unit | Route | instances/edit/personalien/projektverfasser-planer",
  function(hooks) {
    setupTest(hooks);

    test("it exists", function(assert) {
      let route = this.owner.lookup(
        "route:instances/edit/personalien/projektverfasser-planer"
      );
      assert.ok(route);
    });
  }
);
