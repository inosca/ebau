import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | work-item-list-v2/item", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<WorkItemListV2::Item />`);

    assert.dom().hasText("");

    // Template block usage:
    await render(hbs`<WorkItemListV2::Item>
  template block text
</WorkItemListV2::Item>`);

    assert.dom().hasText("template block text");
  });
});
