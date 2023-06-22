import { render, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import id from "dummy/tests/helpers/graphql-id";
import mainConfig from "ember-ebau-core/config/main";

module("Integration | Component | decision/appeal-button", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(function () {
    this.hasAppeal = false;
    this.field = { question: { raw: { label: "Beschwerde eingegangen" } } };

    this.instanceStates = {
      coordination: this.server.create("instance-state"),
      finished: this.server.create("instance-state"),
      sb1: this.server.create("instance-state"),
    };

    mainConfig.instanceStates = Object.entries(this.instanceStates).reduce(
      (obj, [key, state]) => {
        return { ...obj, [key]: parseInt(state.id) };
      },
      {}
    );

    this.server.post("/graphql", () => {
      return {
        data: {
          allCases: {
            edges: [
              {
                node: {
                  id: id("Case"),
                  meta: { "has-appeal": this.hasAppeal },
                },
              },
            ],
          },
        },
      };
    });

    this.initialize = (current, previous, hasAppeal = false) => {
      this.instance = this.server.create("instance", {
        instanceState:
          this.instanceStates[current] ?? this.server.create("instance-state"),
        previousInstanceState:
          this.instanceStates[previous] ?? this.server.create("instance-state"),
      });
      this.hasAppeal = hasAppeal;
    };
  });

  test.each(
    "it renders only if correct states are given",
    [
      [null, null, false, false],
      ["sb1", "coordination", false, true],
      ["finished", "coordination", false, true],
      ["finished", "coordination", true, false],
    ],
    async function (assert, [current, previous, hasAppeal, hasButton]) {
      this.initialize(current, previous, hasAppeal);

      await render(
        hbs`<Decision::AppealButton @field={{this.field}} @context={{hash instanceId=this.instance.id}} />`
      );

      if (hasButton) {
        assert.dom("button").exists();
      } else {
        assert.dom("button").doesNotExist();
      }
    }
  );

  test("it redirects after successful appeal", async function (assert) {
    assert.expect(4);

    this.initialize("finished", "coordination");

    this.server.post(
      `/api/v1/instances/${this.instance.id}/appeal`,
      () => {
        assert.step("request");
        return { data: { id: 99 } };
      },
      201
    );

    this.redirect = (id) => {
      assert.strictEqual(id, 99);
      assert.step("redirect");
    };

    await render(hbs`
      <Decision::AppealButton
        @field={{this.field}}
        @context={{hash instanceId=this.instance.id}}
        @redirectTo={{this.redirect}}
      />
    `);

    await click("button");

    // Confirm dialog
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    await waitFor("button:not([disabled])");

    assert.verifySteps(["request", "redirect"]);
  });
});
