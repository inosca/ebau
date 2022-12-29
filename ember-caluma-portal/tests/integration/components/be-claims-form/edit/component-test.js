import { render } from "@ember/test-helpers";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, skip } from "qunit";

module("Integration | Component | be-claims-form/edit", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<BeClaimsForm::Edit />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <BeClaimsForm::Edit>
        template block text
      </BeClaimsForm::Edit>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
