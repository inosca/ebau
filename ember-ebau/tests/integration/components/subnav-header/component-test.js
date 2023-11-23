import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "ebau/tests/helpers";

module("Integration | Component | subnav-header", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<SubnavHeader />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <SubnavHeader>
        template block text
      </SubnavHeader>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
