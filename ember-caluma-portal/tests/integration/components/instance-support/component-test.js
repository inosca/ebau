import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | instance-support", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<InstanceSupport />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <InstanceSupport>
        template block text
      </InstanceSupport>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
