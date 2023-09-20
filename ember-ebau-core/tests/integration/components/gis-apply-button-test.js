import { click, render, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | gis-apply-button", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it disables the button", async function (assert) {
    await render(hbs`<GisApplyButton @disabled={{true}} />`);

    assert.dom("[data-test-apply]").exists();
    assert.dom("[data-test-apply]").isDisabled();
  });

  test("it can apply API data", async function (assert) {
    this.params = { x: 123, y: 456 };
    this.document = {
      findField() {
        return {
          answer: { value: null },
          save: {
            perform() {
              assert.step("save-field");
            },
          },
        };
      },
    };

    this.server.get("/api/v1/gis/data", (_, request) => {
      assert.deepEqual(
        Object.keys(request.queryParams),
        Object.keys(this.params),
      );

      return {
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
      .dom("[data-test-gis-data-row]:nth-of-type(1) [data-test-gis-data-label]")
      .hasText("Some Question");
    assert
      .dom("[data-test-gis-data-row]:nth-of-type(1) [data-test-gis-data-value]")
      .hasText("My value");

    // Table row 1
    assert
      .dom("[data-test-gis-data-row]:nth-of-type(2) [data-test-gis-data-label]")
      .hasText('Some Table t:so-gis.row-count:("count":1)');
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
      .dom("[data-test-gis-data-row]:nth-of-type(3) [data-test-gis-data-label]")
      .hasText('Some Table t:so-gis.row-count:("count":2)');
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

    assert.verifySteps(["save-field", "save-field"]);
  });
});
