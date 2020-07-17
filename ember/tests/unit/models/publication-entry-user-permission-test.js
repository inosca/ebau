import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | publication-entry-user-permission", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("publication-entry-user-permission", {});
    assert.ok(model);
  });
});
