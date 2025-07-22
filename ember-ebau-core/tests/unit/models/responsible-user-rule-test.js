import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | responsible user rule", function (hooks) {
  setupTest(hooks);

  test("it computes type", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("responsible-user-rule", {});

    assert.strictEqual(model.type, "municipalities");

    model.applicationTypes = [store.createRecord("application-type")];
    assert.strictEqual(model.type, "application-types");

    model.applicationTypes = [];
    model.municipalities = [store.createRecord("public-service")];
    assert.strictEqual(model.type, "municipalities");
  });
});
