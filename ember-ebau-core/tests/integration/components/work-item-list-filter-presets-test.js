import { getOwner } from "@ember/application";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t, setLocale } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | work-item-list-filter-presets",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    test("it renders", async function (assert) {
      setLocale("de");
      this.ebauModules = getOwner(this).lookup("service:ebauModules");
      this.ebauModules.serviceName = "service-test";
      this.ebauModules.serviceGroupName = "service-group-test";

      const preset1 = this.server.create("work-item-list-filter-preset", {
        name: () => ({ de: "preset-1" }),
        category: "STANDARD",
      });

      const preset2 = this.server.create("work-item-list-filter-preset", {
        name: () => ({ de: "preset-2" }),
        category: "SERVICE",
      });

      const preset3 = this.server.create("work-item-list-filter-preset", {
        name: () => ({ de: "preset-3" }),
        category: "SERVICE_GROUP",
      });

      await render(hbs`<WorkItemListFilterPresets />`);

      assert.dom("[data-test-presets-category]").exists({ count: 3 });
      assert.dom("[data-test-preset]").exists({ count: 3 });

      assert
        .dom("[data-test-presets-category]:nth-of-type(1)")
        .hasText(t("workItems.presets.standard"));
      assert.dom(`[data-test-preset="${preset1.id}"]`).hasText("preset-1");

      assert
        .dom("[data-test-presets-category]:nth-of-type(2)")
        .hasText(
          t("workItems.presets.service", { serviceName: "service-test" }),
        );
      assert.dom(`[data-test-preset="${preset2.id}"]`).hasText("preset-2");

      assert.dom("[data-test-presets-category]:nth-of-type(3)").hasText(
        t("workItems.presets.serviceGroup", {
          serviceGroupName: "service-group-test",
        }),
      );
      assert.dom(`[data-test-preset="${preset3.id}"]`).hasText("preset-3");

      assert.dom("[data-test-presets-reset]").exists();
    });
  },
);
