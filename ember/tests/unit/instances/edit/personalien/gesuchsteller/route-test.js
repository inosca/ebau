import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Route | instances/edit/personalien/gesuchsteller", function(
  hooks
) {
  setupTest(hooks);

  test("it exists", function(assert) {
    let route = this.owner.lookup(
      "route:instances/edit/personalien/gesuchsteller"
    );
    assert.ok(route);
  });
});
