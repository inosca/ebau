import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | work-item-list", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.set("query", { value: [] });

    await render(
      hbs`<WorkItemList @query={{this.query}} @columns={{(array)}} />`
    );

    assert.dom("table").exists();
    assert.dom("th").exists({ count: 2 });
  });
});
