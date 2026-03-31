import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | applicant-confirmations/widget",
  function (hooks) {
    setupRenderingTest(hooks);

    skip("it renders", async function (assert) {
      // Set any properties with this.set('myProperty', 'value');
      // Handle any actions with this.set('myAction', function(val) { ... });

      await render(hbs`<ApplicantConfirmations::Widget />`);

      assert.dom().hasText("");

      // Template block usage:
      await render(hbs`<ApplicantConfirmations::Widget>
  template block text
</ApplicantConfirmations::Widget>`);

      assert.dom().hasText("template block text");
    });
  },
);
