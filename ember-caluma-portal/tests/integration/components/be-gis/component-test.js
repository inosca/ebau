import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | be-gis", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    await render(hbs`<BeGis />`);
    assert.ok(this.element);
  });
});
