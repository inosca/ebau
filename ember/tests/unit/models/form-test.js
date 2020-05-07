import { run } from "@ember/runloop";
import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | form", function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function(assert) {
    const store = this.owner.lookup("service:store");
    const model = run(() => store.createRecord("form", {}));
    assert.ok(model);
  });
});
