import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | case-filter", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<CaseFilter />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <CaseFilter>
        template block text
      </CaseFilter>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
