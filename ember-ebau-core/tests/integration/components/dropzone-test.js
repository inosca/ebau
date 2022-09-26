import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | dropzone", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Dropzone />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <Dropzone>
        template block text
      </Dropzone>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
