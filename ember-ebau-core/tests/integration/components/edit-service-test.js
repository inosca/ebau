import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | edit-service", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<EditService />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`<EditService>
  template block text
</EditService>`);

    assert.dom(this.element).hasText("template block text");
  });
});
