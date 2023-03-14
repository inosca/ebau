import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import id from "dummy/tests/helpers/graphql-id";

module("Integration | Component | decision/info-appeal", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(function () {
    this.instanceStates = {
      coordination: this.server.create("instance-state", {
        name: "In Koordination",
      }),
      circulationInit: this.server.create("instance-state", {
        name: "Zirkulation initialisieren",
      }),
      finished: this.server.create("instance-state", { name: "Abgeschlossen" }),
      sb1: this.server.create("instance-state", {
        name: "Selbstdeklaration 1 (SB1)",
      }),
    };

    this.owner.resolveRegistration("config:environment").APPLICATION = {
      instanceStates: Object.entries(this.instanceStates).reduce(
        (obj, [key, state]) => {
          return { ...obj, [key]: parseInt(state.id) };
        },
        {}
      ),
    };

    this.field = { document: { findAnswer: () => this.decision } };

    this.server.post("/graphql", () => {
      return {
        data: {
          allCases: {
            edges: [
              {
                node: {
                  id: id("Case"),
                  document: {
                    id: id("Document"),
                    source: {
                      id: id("Document"),
                      case: {
                        id: id("Case"),
                        meta: { "camac-instance-id": this.sourceInstance.id },
                      },
                    },
                  },
                },
              },
            ],
          },
        },
      };
    });

    this.initialize = (decision, previousInstanceState) => {
      this.decision = `decision-decision-assessment-appeal-${decision}`;
      this.sourceInstance = this.server.create("instance", {
        previousInstanceStateId: previousInstanceState.id,
      });
    };
  });

  test.each(
    "it renders",
    [
      ["confirmed", "sb1", "sb1", "success"],
      ["confirmed", "coordination", "finished", "success"],
      ["changed", "sb1", "finished", "danger"],
      ["changed", "coordination", "sb1", "danger"],
      ["rejected", "sb1", "circulationInit", "danger"],
      ["rejected", "coordination", "circulationInit", "danger"],
    ],
    async function (
      assert,
      [decision, previousInstanceState, expectedInstanceState, expectedColor]
    ) {
      this.initialize(decision, this.instanceStates[previousInstanceState]);

      await render(
        hbs`<Decision::InfoAppeal @context={{hash instanceId=1}} @field={{this.field}}/>`
      );

      assert.dom(".uk-alert").hasClass(`uk-alert-${expectedColor}`);

      const expectedName = this.instanceStates[expectedInstanceState].name;
      assert
        .dom(".uk-alert")
        .hasText(`t:decision.appeal.${decision}:("status":"${expectedName}")`);
    }
  );
});
