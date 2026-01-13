import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Helper | ebau-modules-value", function (hooks) {
  setupRenderingTest(hooks);

  test("it works", async function (assert) {
    const service = this.owner.lookup("service:ebau-modules");

    service.instanceId = 999;

    await render(hbs`{{ebau-modules-value "instanceId"}}`);
    assert.dom().hasText("999");

    await render(hbs`{{ebau-modules-value "someUnknownProperty"}}`);
    assert.dom().hasText("");
  });
});
