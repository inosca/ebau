import { render } from "@ember/test-helpers";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | be-subnav-link", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(
      hbs`<BeSubnavLink @query={{hash}} @label="Test" @active={{true}} />`
    );

    assert.dom("span").hasText("Test");
    assert.dom("span").hasAttribute("role", "heading");
    assert.dom("span").hasAttribute("aria-level", "1");
  });
});
