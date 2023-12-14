import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | case-filter/base", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Template block usage:
    await render(hbs`
      <CaseFilter::Base @filterName="instanceState">
        template block text
      </CaseFilter::Base>
    `);

    assert.ok(this.element.textContent.trim());
  });
});
