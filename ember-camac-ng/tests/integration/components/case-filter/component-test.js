import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { module, skip } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | case-filter", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<CaseFilter />`);

    assert.ok(this.element.textContent.trim());
  });
});
