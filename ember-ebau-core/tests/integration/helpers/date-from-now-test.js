import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { DateTime } from "luxon";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Helper | date-from-now", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function () {
    this.date = DateTime.now().minus({ days: 6 });
  });

  test("it renders with a date", async function (assert) {
    this.value = this.date.toJSDate();

    await render(hbs`{{date-from-now this.value}}`);

    assert.dom(this.element).hasText("vor 5 Tagen");
  });

  test("it renders with a string", async function (assert) {
    this.value = this.date.toISO();

    await render(hbs`{{date-from-now this.value}}`);

    assert.dom(this.element).hasText("vor 5 Tagen");
  });

  test("it renders without a value", async function (assert) {
    await render(hbs`{{date-from-now null}}`);

    assert.dom(this.element).hasText("");
  });

  test("it can force using the start of the day", async function (assert) {
    this.value = this.date.toJSDate();

    await render(hbs`{{date-from-now this.value startOfDay=true}}`);

    assert.dom(this.element).hasText("vor 6 Tagen");
  });
});
