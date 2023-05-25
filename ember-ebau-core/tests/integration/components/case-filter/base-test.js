import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | case-filter/base", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<CaseFilter::Base />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <CaseFilter::Base>
        template block text
      </CaseFilter::Base>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
