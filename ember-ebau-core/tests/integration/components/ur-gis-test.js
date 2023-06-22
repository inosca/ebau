import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { module } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { testUR } from "dummy/tests/helpers/scenarios";

module("Integration | Component | ur-gis", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  testUR("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<UrGis />`);

    assert.ok(this.element.textContent.trim());
  });
});
