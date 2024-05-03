import { render, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import id from "dummy/tests/helpers/graphql-id";
import { testBE } from "dummy/tests/helpers/scenarios";
import mainConfig from "ember-ebau-core/config/main";

module("Integration | Component | decision/appeal-button", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.meta = {};
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
      {},
    );

    this.server.post("/graphql", () => {
      return {
        data: {
          allCases: {
            edges: [
              {
                node: {
                  id: id("Case"),
                  meta: this.meta,
                },
              },
            ],
          },
        },
      };
    });

    this.initialize = (current, previous, meta = {}) => {
      this.instance = this.server.create("instance", {
        instanceState:
          this.instanceStates[current] ?? this.server.create("instance-state"),
        previousInstanceState:
          this.instanceStates[previous] ?? this.server.create("instance-state"),
      });
      this.meta = meta;
    };
  });

  testBE.each(
    "it renders only if correct states are given",
    [
      [null, null, {}, false],
      ["sb1", "coordination", {}, true],
      ["finished", "coordination", {}, true],
      ["finished", "coordination", { "is-appeal": true }, false],
      ["finished", "coordination", { "has-appeal": true }, false],
    ],
    async function (assert, [current, previous, meta, hasButton]) {
      this.initialize(current, previous, meta);

      await render(
        hbs`<Decision::AppealButton @field={{this.field}} @context={{hash instanceId=this.instance.id}} />`,
      );

      if (hasButton) {
        assert.dom("button").exists();
      } else {
        assert.dom("button").doesNotExist();
      }
    },
  );

  testBE("it redirects after successful appeal", async function (assert) {
    this.initialize("finished", "coordination");

    this.server.post(
      `/api/v1/instances/${this.instance.id}/appeal`,
      () => {
        assert.step("request");
        return { data: { id: 99 } };
      },
      201,
    );

    this.owner.lookup("service:ebau-modules").redirectToInstance = (
      instanceId,
    ) => {
      assert.strictEqual(instanceId, 99);
      assert.step("redirect");
    };

    await render(hbs`
      <Decision::AppealButton
        @field={{this.field}}
        @context={{hash instanceId=this.instance.id}}
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
