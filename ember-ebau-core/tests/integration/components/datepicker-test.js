import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | datepicker", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Datepicker />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <Datepicker>
        template block text
      </Datepicker>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
