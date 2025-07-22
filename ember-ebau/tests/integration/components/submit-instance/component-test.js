import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "ebau/tests/helpers";

module("Integration | Component | submit-instance", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    await render(hbs`<SubmitInstance />`);

    assert.ok(this.element.textContent);
  });
});
