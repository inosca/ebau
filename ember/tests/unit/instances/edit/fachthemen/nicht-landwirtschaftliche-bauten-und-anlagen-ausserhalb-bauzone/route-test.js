import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module(
  "Unit | Route | instances/edit/fachthemen/nicht-landwirtschaftliche-bauten-und-anlagen-ausserhalb-bauzone",
  function(hooks) {
    setupTest(hooks);

    test("it exists", function(assert) {
      const route = this.owner.lookup(
        "route:instances/edit/fachthemen/nicht-landwirtschaftliche-bauten-und-anlagen-ausserhalb-bauzone"
      );
      assert.ok(route);
    });
  }
);
