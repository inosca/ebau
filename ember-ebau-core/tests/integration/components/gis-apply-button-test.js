import { click, render, settled, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Integration | Component | gis-apply-button", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupFeatures(hooks);

  test("it disables the button", async function (assert) {
    await render(hbs`<GisApplyButton @disabled={{true}} />`);

    assert.dom("[data-test-apply]").exists();
    assert.dom("[data-test-apply]").isDisabled();
  });

  test.each(
    "it can apply API data",
    [[["gis.v3"]], [["gis.legacy_api"]]],
    async function (assert, [enabledFeature]) {
      this.features.disableAll();
      this.features.enable(...enabledFeature);

      this.params = { x: 123, y: 456 };
      this.document = {
        findField() {
          return {
            answer: { value: null },
            refreshAnswer: {
              linked: () => ({
                perform: () => assert.step("refresh-answer"),
              }),
            },
          };
        },
      };

      const dataResponse = {
        data: {
          "some-question": { label: "Some Question", value: "My value" },
          "some-table": {
            label: "Some Table",
            form: "some-table-form",
            value: [
              {
                "some-table-question": {
                  label: "Some Table Question",
                  value: "My 2nd value",
                },
              },
              {
                "some-table-question": {
                  label: "Some Table Question",
                  value: "My 3rd value",
                },
              },
            ],
          },
        },
      };

      this.server.get("/api/v1/gis/data", (_, request) => {
        assert.deepEqual(
          Object.keys(request.queryParams),
          Object.keys(this.params),
        );

        if (hasFeature("gis.v3")) {
          return { task_id: "1234" };
        }
        return dataResponse;
      });

      this.server.get("/api/v1/gis/data/:id", (_, request) => {
        assert.deepEqual(Object.keys(request.params.id), Object.keys("1234"));

        return dataResponse;
      });

      this.server.post("/api/v1/gis/apply", () => {
        assert.step("apply");
        return { questions: Object.keys(dataResponse.data) };
      });

      await render(hbs`<GisApplyButton
      @disabled={{false}}
      @params={{this.params}}
      @document={{this.document}}
    />`);

      assert.dom("[data-test-apply]").exists();

      await click("[data-test-apply]");
      await waitFor("[data-test-gis-data-row]");

      // Root level questions
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(1) [data-test-gis-data-label]",
        )
        .hasText("Some Question");
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(1) [data-test-gis-data-value]",
        )
        .hasText("My value");

      // Table row 1
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(2) [data-test-gis-data-label]",
        )
        .hasText(`Some Table ${t("gis.row-count", { count: 1 })}`);
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(2) [data-test-gis-data-table-label]",
        )
        .hasText("Some Table Question");
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(2) [data-test-gis-data-table-value]",
        )
        .hasText("My 2nd value");

      // Table row 2
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(3) [data-test-gis-data-label]",
        )
        .hasText(`Some Table ${t("gis.row-count", { count: 2 })}`);
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(3) [data-test-gis-data-table-label]",
        )
        .hasText("Some Table Question");
      assert
        .dom(
          "[data-test-gis-data-row]:nth-of-type(3) [data-test-gis-data-table-value]",
        )
        .hasText("My 3rd value");

      await click("[data-test-confirm]");

      // eslint-disable-next-line ember/no-settled-after-test-helper
      await settled();

      assert.verifySteps(["apply", "refresh-answer", "refresh-answer"]);
    },
  );
});
