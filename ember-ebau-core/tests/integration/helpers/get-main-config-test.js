import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import mainConfig from "ember-ebau-core/config/main";

module("Integration | Helper | get-main-config", function (hooks) {
  setupRenderingTest(hooks);

  test("it returns the value from the main config", async function (assert) {
    await render(hbs`{{get-main-config "documentBackend"}}`);

    assert.dom(this.element).hasText(mainConfig.documentBackend);

    await render(hbs`{{get-main-config "rejection.instanceState"}}`);

    assert.dom(this.element).hasText(mainConfig.rejection?.instanceState);
  });
});
