import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Route | instances/edit/konzession-fur-wasserentnahme", function(
  hooks
) {
  setupTest(hooks);

  test("it exists", function(assert) {
    let route = this.owner.lookup(
      "route:instances/edit/konzession-fur-wasserentnahme"
    );
    assert.ok(route);
  });
});
