import { module, skip } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Component | in-viewport", function(hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function(assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`{{in-viewport}}`);

    assert.equal(this.element.textContent.trim(), "");

    // Template block usage:
    await render(hbs`
      {{#in-viewport}}
        template block text
      {{/in-viewport}}
    `);

    assert.equal(this.element.textContent.trim(), "template block text");
  });
});
