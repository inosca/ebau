import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import setupFeatures from "dummy/tests/helpers/features";

module("Integration | Helper | has-feature", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);

  test("it renders", async function (assert) {
    this.features.enable(
      "some.feature",
      "someotherfeature",
      "some.nested.feature",
    );

    await render(hbs`{{if (has-feature "some.feature") "enabled" "disabled"}}`);
    assert.dom(this.element).hasText("enabled");
    await render(
      hbs`{{if (has-feature "someotherfeature") "enabled" "disabled"}}`,
    );
    assert.dom(this.element).hasText("enabled");
    await render(
      hbs`{{if (has-feature "some.nested.feature") "enabled" "disabled"}}`,
    );
    assert.dom(this.element).hasText("enabled");

    this.features.disable(
      "some.feature",
      "someotherfeature",
      "some.nested.feature",
    );

    await render(hbs`{{if (has-feature "some.feature") "enabled" "disabled"}}`);
    assert.dom(this.element).hasText("disabled");
    await render(
      hbs`{{if (has-feature "someotherfeature") "enabled" "disabled"}}`,
    );
    assert.dom(this.element).hasText("disabled");
    await render(
      hbs`{{if (has-feature "some.nested.feature") "enabled" "disabled"}}`,
    );
    assert.dom(this.element).hasText("disabled");
  });
});
