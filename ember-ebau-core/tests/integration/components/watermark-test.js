import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Integration | Component | watermark", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);

  test("it renders", async function (assert) {
    this.features.enable("watermark");

    await render(hbs`<Watermark />`);

    assert.dom(this.element).hasText("dev");
  });
});
