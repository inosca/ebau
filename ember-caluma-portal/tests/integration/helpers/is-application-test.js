import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";
import testIf from "caluma-portal/tests/helpers/test-if";

module("Integration | Helper | is-application", function (hooks) {
  setupRenderingTest(hooks);

  testIf("be")("it works", async function (assert) {
    await render(hbs`{{#if (is-application "be")}}Hello{{/if}}`);

    assert.equal(this.element.textContent.trim(), "Hello");
  });
});
