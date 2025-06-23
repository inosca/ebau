import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | work-item-list-filter-presets/presets-category",
  function (hooks) {
    setupRenderingTest(hooks);

    test("it renders", async function (assert) {
      this.presets = [
        {
          id: "1",
          name: "preset-1",
          query: { "key-1": "value-1" },
        },
        {
          id: "2",
          name: "preset-2",
          query: { "key-2": "value-2" },
        },
      ];

      await render(hbs`<WorkItemListFilterPresets::PresetsCategory
  @label="test"
  @presets={{this.presets}}
  @selected="preset-2"
/>`);

      assert.dom("label").hasText("test");
      assert.dom("[data-test-preset]").exists({ count: 2 });
      assert.dom(`[data-test-preset="1"]`).hasText("preset-1");
      assert.dom(`[data-test-preset="2"]`).hasText("preset-2");

      assert
        .dom(`[data-test-preset="1"]`)
        .hasAttribute("href", "/work-items?key-1=value-1");
      assert
        .dom(`[data-test-preset="2"]`)
        .hasAttribute("href", "/work-items?key-2=value-2");
    });
  },
);
