import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setFlatpickrDate } from "ember-flatpickr/test-support/helpers";
import { module, test } from "qunit";
import { fake } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | publication-fill-end-date", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function () {
    this.endField = {
      answer: {
        value: null,
      },
      save: {
        perform: fake(),
      },
    };

    this.startField = {
      raw: {
        question: {
          meta: {
            "fill-end-date": {
              question: "end-question",
              delta: 10,
            },
          },
        },
      },
      answer: {
        value: "2025-02-24",
      },
      document: {
        findField: () => this.endField,
      },
    };
  });

  test("it renders", async function (assert) {
    await render(hbs`<PublicationFillEndDate @field={{this.startField}} />`);

    assert.dom("input[type=hidden]").hasValue("2025-02-24");
    assert.dom("input[type=text]").hasValue("24.02.2025");
  });

  test("it sets the end date when setting the start date", async function (assert) {
    this.onSave = fake();

    await render(
      hbs`<PublicationFillEndDate @field={{this.startField}} @onSave={{this.onSave}} />`,
    );

    await setFlatpickrDate("input", "2025-01-01");

    // On save function was called with the input date
    assert.strictEqual(this.onSave.callCount, 1);
    assert.strictEqual(this.onSave.firstArg, "2025-01-01");

    // Value of end question was calculated and saved
    assert.strictEqual(this.endField.answer.value, "2025-01-11");
    assert.strictEqual(this.endField.save.perform.callCount, 1);
  });
});
