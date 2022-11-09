import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | snippets", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    this.set("field", { answer: { value: "" } });

    await render(hbs`
      <Snippets @field={{@field}}>template block text</Snippets>
    `);

    assert.ok(this.element.textContent.includes("template block text"));
  });
});
