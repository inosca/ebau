import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | direct-inquiry-info", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<DirectInquiryInfo />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`<DirectInquiryInfo>
  template block text
</DirectInquiryInfo>`);

    assert.dom(this.element).hasText("template block text");
  });
});