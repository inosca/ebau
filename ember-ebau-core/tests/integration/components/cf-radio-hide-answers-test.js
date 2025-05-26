import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | cf-radio-hide-answers", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function () {
    this.set("question", {
      slug: "question-slug",
    });
    this.set("options", [
      {
        slug: "value-1",
        label: "Label 1",
        disabled: false,
      },
      {
        slug: "value-2",
        label: "Label 2",
        disabled: false,
      },
      {
        slug: "value-3",
        label: "Label 3",
        disabled: false,
      },
    ]);
  });

  test("it renders a default options list", async function (assert) {
    this.field = {
      options: this.options,
      answer: {
        value: null,
      },
    };

    await render(hbs`<CfRadioHideAnswers @field={{this.field}} />`);
    assert.dom("[data-test-option]").exists({ count: 3 });
  });

  test("it hides configured options", async function (assert) {
    this.field = {
      options: this.options,
      question: {
        ...this.question,
        raw: {
          meta: {
            hiddenAnswers: ["value-1", "value-2"],
            alternativeText: {
              "value-1": "translation.value-1",
              "value-2": "translation.value-2",
            },
          },
        },
      },
      answer: {
        value: null,
      },
    };

    await render(hbs`<CfRadioHideAnswers @field={{this.field}} />`);
    assert.dom("[data-test-option]").exists({ count: 1 });
  });

  test("it shows an alternative text if the answer matches", async function (assert) {
    this.field = {
      options: this.options,
      question: {
        ...this.question,
        raw: {
          meta: {
            hiddenAnswers: ["value-1", "value-2"],
            alternativeText: {
              "value-1": "translation.value-1",
              "value-2": "translation.value-2",
            },
          },
        },
      },
      answer: {
        value: "value-2",
      },
    };

    await render(hbs`<CfRadioHideAnswers @field={{this.field}} />`);
    assert.dom("[data-test-alternative-text]").exists();
    assert
      .dom("[data-test-alternative-text]")
      .containsText("translation.value-2");
    assert.dom("[data-test-option]").exists({ count: 0 });
  });
});
