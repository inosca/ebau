import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | aria-heading", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.enabled = true;

    await render(
      hbs`<AriaHeading @enabled={{this.enabled}} @level={{this.level}}>Test</AriaHeading>`
    );

    assert.dom("span").hasText("Test");
    assert.dom("span").hasAttribute("role", "heading");
    assert.dom("span").hasAttribute("aria-level", "1");

    this.set("level", 2);

    assert.dom("span").hasAttribute("aria-level", "2");

    this.set("enabled", false);

    assert.dom("span").doesNotExist();
    assert.dom(this.element).hasText("Test");
  });
});
