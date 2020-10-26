import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | case-filter/input", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    this.set("update", () => null);
    await render(hbs`<CaseFilter::Input @updateFilter={{update}} />`);

    assert.ok(this.element.textContent.trim());
  });
});
