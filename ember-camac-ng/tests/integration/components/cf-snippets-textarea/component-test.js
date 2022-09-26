import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | cf-snippets-textarea", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    this.field = { answer: { value: "" } };

    await render(hbs`<CfSnippetsTextarea @field={{@field}}/>`);

    assert.dom(this.element).hasText("t:global.empty:()");
  });
});
