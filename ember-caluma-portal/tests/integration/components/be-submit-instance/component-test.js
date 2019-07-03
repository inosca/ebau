import { module, skip } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Component | be-submit-instance", function(hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function(assert) {
    await render(hbs`{{be-submit-instance}}`);

    assert.ok(this.element.textContent);
  });
});
