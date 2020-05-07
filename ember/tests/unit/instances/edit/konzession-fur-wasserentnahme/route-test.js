import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | instances/edit/konzession-fur-wasserentnahme", function(
  hooks
) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const route = this.owner.lookup(
      "route:instances/edit/konzession-fur-wasserentnahme"
    );
    assert.ok(route);
  });
});
