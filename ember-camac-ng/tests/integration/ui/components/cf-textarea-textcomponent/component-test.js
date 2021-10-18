import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import setupMirage from "ember-cli-mirage/test-support/setup-mirage";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | cf-textarea-textcomponent", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    this.field = { answer: { value: "" } };

    await render(hbs`<CfTextareaTextcomponent @field={{@field}}/>`);

    assert.dom(this.element).hasText("t:global.empty:()");
  });
});
