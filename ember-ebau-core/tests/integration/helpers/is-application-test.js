import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import mainConfig from "ember-ebau-core/config/main";

module("Integration | Helper | is-application", function (hooks) {
  setupRenderingTest(hooks);

  test("it matches the configured application", async function (assert) {
    this.name = mainConfig.name;

    await render(hbs`{{#if (is-application this.name)}}Hello{{/if}}`);

    assert.dom(this.element).hasText("Hello");
  });

  test("it matches any of the given applications", async function (assert) {
    this.name = mainConfig.name;

    await render(
      hbs`{{#if (is-application "some-other-application" this.name)}}Hello{{/if}}`,
    );

    assert.dom(this.element).hasText("Hello");
  });

  test("it does not match another application", async function (assert) {
    await render(
      hbs`{{#if (is-application "some-other-application")}}Hello{{/if}}`,
    );

    assert.dom(this.element).hasNoText();
  });
});
