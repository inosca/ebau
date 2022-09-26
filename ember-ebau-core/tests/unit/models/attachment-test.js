import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | attachment", function (hooks) {
  setupTest(hooks);
  setupIntl(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("attachment", {});
    assert.ok(model);
  });

  test("it renders the name replaced", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("attachment", {
      name: "test.pdf",
      context: { isReplaced: false },
    });
    assert.strictEqual(model.get("name"), "test.pdf");

    model.context.isReplaced = true;
    assert.strictEqual(
      model.displayNameOrReplaced.string,
      "<del>test.pdf</del> t:link-attachments.replaced:()"
    );
  });
});
