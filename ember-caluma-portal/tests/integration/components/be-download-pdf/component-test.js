import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Component | be-download-pdf", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function(assert) {
    await render(
      hbs`{{be-download-pdf field=(hash question=(hash label="Test"))}}`
    );

    assert.dom("button").hasText("Test");
  });
});
