import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";
import { fake } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | eeba-confirmation", function (hooks) {
  setupRenderingTest(hooks);

  this.defaultValues = {
    "eeba-state": null,
    "eeba-required": null,
    "eeba-integration-id": null,
    "eeba-web-url": null,
    "eeba-is-dirty": null,
    "eeba-confirmation": null,
  };
  this.values = {};
  this.meta = {
    "eeba-state": {
      widgetOverride: "cf-field/input/hidden",
      eebaLinkedFields: [
        "juristische-person-gesuchstellerin",
        "name-juristische-person-gesuchstellerin",
        "name-gesuchstellerin",
        "vorname-gesuchstellerin",
        "strasse-gesuchstellerin",
        "nummer-gesuchstellerin",
        "plz-gesuchstellerin",
        "ort-gesuchstellerin",
        "e-mail-gesuchstellerin",
        "telefon-oder-mobile-gesuchstellerin",
        "hinweis-personalien",
        "gemeinde",
        "parzellennummer",
        "baurecht-nummer",
        "e-grid-nr",
        "rueckbaumaterial-volumen",
        "abgetragener-oberboden-volumen",
        "aushub-volumen",
        "strasse-belag-volumen",
        "gleisaushub-volumen",
        "baujahr-aeltestes-betroffenes-objekt",
        "das-bauvorhaben-befindet-sich-in-kataster-belasteter-standorte",
        "eeba-is-dirty",
      ],
    },
  };

  hooks.beforeEach(function () {
    // reset default values
    this.values = { ...this.defaultValues };

    // emulate related fields for component
    this.field = {
      raw: {
        question: {
          meta: {},
        },
      },
      answer: {
        value: null,
      },
      document: {
        findField: (slug) => {
          if (typeof this.values[slug] === "undefined") {
            return null;
          }

          return {
            answer: { value: this.values[slug] || null },
            question: {
              raw: {
                meta: this.meta[slug] || {},
              },
            },
          };
        },
      },
      save: {
        perform: fake(),
      },
    };
  });

  test("it renders", async function (assert) {
    await render(hbs`<EebaConfirmation @field={{this.field}} />`);
    assert.dom("[data-test-eeba-check]").exists();
    assert.dom("[data-test-eeba-check]").isNotDisabled();
  });

  test.each(
    "it shows the correct description or hidden if eeba-required is empty",
    [
      ["", ""],
      [
        "eeba-required-ja",
        "Für Ihr Baugesuch ist eine elektronische Entsorgungserklärung für Bauabfälle (eEBA) nötig. Die eEBA wurde bereits im Hintergrund vorbereitet. Bitte melden Sie sich am eEBA-Onlineservice an, prüfen Sie die Angaben (anfallenden Abfallkategorien und -mengen) und ergänzen oder korrigieren Sie diese falls nötig. Vergessen Sie danach nicht, die eEBA einzureichen und anschliessend Ihr Baugesuch im eBau-Portal zu vervollständigen.",
      ],
      ["eeba-required-nein", "Entsorgungserklärung (eEBA) nicht nötig"],
    ],
    async function (assert, [isRequired, descriptionText]) {
      this.values["eeba-required"] = isRequired;
      await render(hbs`<EebaConfirmation @field={{this.field}} />`);

      if (isRequired === "") {
        assert.dom("[data-test-eeba-description]").doesNotExist();
      } else {
        assert.dom("[data-test-eeba-description]").exists();
        assert
          .dom("[data-test-eeba-description]")
          .containsText(descriptionText);
      }
    },
  );

  test.each(
    /**
     * shouldBeEnabled will be true when these conditions are met:
     *
     * - isInternal is false
     * - isDirty is true OR state is not "completed"
     */
    "it enables the check button only in portal when conditions are met",
    [
      // isInternal, other values don't matter
      [true, false, "completed", false],
      [true, false, "", false],
      [true, true, "completed", false],
      [true, true, "", false],

      // not internal
      [false, false, "completed", false], // already completed and not dirty
      [false, false, "", true], // not completed
      [false, true, "completed", true], // dirty
      [false, true, "", true], // dirty and not completed
    ],
    async function (assert, [isInternal, isDirty, state, shouldBeEnabled]) {
      this.owner.lookup("service:session").isInternal = isInternal === true;

      this.values["eeba-state"] = state;
      this.values["eeba-is-dirty"] = isDirty
        ? "eeba-is-dirty-ja"
        : "eeba-is-dirty-nein";

      await render(hbs`<EebaConfirmation @field={{this.field}} />`);
      assert.dom("[data-test-eeba-check]").exists();

      if (shouldBeEnabled) {
        assert.dom("[data-test-eeba-check]").isNotDisabled();
      } else {
        assert.dom("[data-test-eeba-check]").isDisabled();
      }
    },
  );
});
