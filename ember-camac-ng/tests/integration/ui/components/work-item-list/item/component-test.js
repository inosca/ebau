import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | work-item-list/item", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });
    this.set("workItem", { task: { slug: "" } });

    await render(hbs`<WorkItemList::Item @workItem={{this.workItem}} />`);

    assert.dom("tr").exists();
  });
});
