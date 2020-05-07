import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module(
  "Unit | Route | instances/edit/fachthemen/natur-und-landschaftsschutz",
  function(hooks) {
    setupTest(hooks);

    test("it exists", function(assert) {
      const route = this.owner.lookup(
        "route:instances/edit/fachthemen/natur-und-landschaftsschutz"
      );
      assert.ok(route);
    });
  }
);
