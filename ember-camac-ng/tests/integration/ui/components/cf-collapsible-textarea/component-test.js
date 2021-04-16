import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | cf-collapsible-textarea", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.set("field", { question: { label: "Textarea" } });

    await render(hbs`<CfCollapsibleTextarea @field={{this.field}}/>`);

    assert.dom("textarea").doesNotExist();
    assert.dom("span[icon='chevron-right']").exists();

    await click("a");

    assert.dom("textarea").exists();
    assert.dom("span[icon='chevron-down']").exists();
  });
});
