import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | case-filter/select", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    this.set("update", () => null);
    this.set("options", [{ label: "Option 1", slug: "option-1" }]);
    await render(
      hbs`<CaseFilter::Select @updateFilter={{this.update}} @filterOptions={{this.options}} />`,
    );

    assert.ok(this.element.textContent.trim());
  });
});
