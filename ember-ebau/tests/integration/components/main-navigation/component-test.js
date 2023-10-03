import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { module, skip } from "qunit";

import { setupRenderingTest } from "ebau/tests/helpers";

module("Integration | Component | main-navigation", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  skip("it renders", async function (assert) {
    await render(hbs`<MainNavigation />`);

    assert.dom(this.element).containsText("t:nav.logout:()");
  });
});
