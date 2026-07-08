import { click, render, settled, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | rpg2-import-button", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it disables the button", async function (assert) {
    await render(hbs`<Rpg2ImportButton @disabled={{true}} />`);

    assert.dom("[data-test-rpg2-import]").exists();
    assert.dom("[data-test-rpg2-import]").isDisabled();
  });

  test("it renders the preview, applies on confirm and refreshes the written fields", async function (assert) {
    const instance = this.server.create("instance");
    this.context = { instanceId: instance.id };
    this.field = {
      document: {
        findField: () => ({
          refreshAnswer: {
            linked: () => ({ perform: () => assert.step("refresh-answer") }),
          },
        }),
      },
    };

    const dataResponse = {
      data: {
        "rpg2-bewilligungsgrund": {
          label: "Rechtliche Grundlage RPG / RPV",
          value: "rpg2-bewilligungsgrund-a02",
          displayValue: "A02",
        },
        "rpg2-versiegelte-entsiegelte-flaechen": {
          label: "Versiegelte / entsiegelte Flächen",
          form: "rpg2-versiegelte-entsiegelte-flaechen",
          value: [
            {
              "rpg2-flaeche-quadrat-meter": {
                label: "Fläche (m²)",
                value: "120",
              },
            },
          ],
        },
      },
    };

    this.server.get("/api/v1/instances/1/rpg2-data", () => {
      assert.step("rpg2-data");
      return dataResponse;
    });
    this.server.post("/api/v1/instances/1/rpg2-apply", () => {
      assert.step("rpg2-apply");
      return { questions: Object.keys(dataResponse.data) };
    });

    await render(hbs`<Rpg2ImportButton
  @disabled={{false}}
  @field={{this.field}}
  @context={{this.context}}
/>`);

    await click("[data-test-rpg2-import]");
    await waitFor("[data-test-import-preview-row]");

    // Root level questions
    // Shows displayValue
    assert
      .dom(
        "[data-test-import-preview-row]:nth-of-type(1) [data-test-import-preview-label]",
      )
      .hasText("Rechtliche Grundlage RPG / RPV");
    assert
      .dom(
        "[data-test-import-preview-row]:nth-of-type(1) [data-test-import-preview-value]",
      )
      .hasText("A02");

    // Single table row
    assert
      .dom(
        "[data-test-import-preview-row]:nth-of-type(2) [data-test-import-preview-label]",
      )
      .hasText("Versiegelte / entsiegelte Flächen");
    assert
      .dom(
        "[data-test-import-preview-row]:nth-of-type(2) [data-test-import-preview-table-label]",
      )
      .hasText("Fläche (m²)");
    assert
      .dom(
        "[data-test-import-preview-row]:nth-of-type(2) [data-test-import-preview-table-value]",
      )
      .hasText("120");

    await click("[data-test-rpg2-confirm]");

    // eslint-disable-next-line ember/no-settled-after-test-helper
    await settled();

    assert.verifySteps([
      "rpg2-data",
      "rpg2-apply",
      "refresh-answer",
      "refresh-answer",
    ]);
  });

  test("it does not apply when canceled", async function (assert) {
    const instance = this.server.create("instance");
    this.context = { instanceId: instance.id };

    this.server.get("/api/v1/instances/1/rpg2-data", () => {
      assert.step("rpg2-data");
      return {
        data: {
          "rpg2-bewilligungsgrund": {
            label: "Rechtliche Grundlage RPG / RPV",
            value: "rpg2-bewilligungsgrund-a02",
            displayValue: "A02",
          },
        },
      };
    });
    this.server.post("/api/v1/instances/1/rpg2-apply", () => {
      assert.step("rpg2-apply");
      return { questions: [] };
    });

    await render(
      hbs`<Rpg2ImportButton @disabled={{false}} @context={{this.context}} />`,
    );

    await click("[data-test-rpg2-import]");
    await waitFor("[data-test-import-preview-row]");
    await click("[data-test-rpg2-cancel]");

    // eslint-disable-next-line ember/no-settled-after-test-helper
    await settled();
    // No apply step
    assert.verifySteps(["rpg2-data"]);
  });
});
