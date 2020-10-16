import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | case-filter/base", function(hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function(assert) {
    // Template block usage:
    await render(hbs`
      <CaseFilter::Base @filterName="instanceState">
        template block text
      </CaseFilter::Base>
    `);

    assert.ok(this.element.textContent.trim());
  });
});
