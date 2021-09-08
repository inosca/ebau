import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | instances/edit/grundinformationen/gwr-v2", function (
  hooks
) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup(
      "route:instances/edit/grundinformationen/gwr-v2"
    );
    assert.ok(route);
  });
});
