import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { DateTime } from "luxon";
import { module, test } from "qunit";

module("Integration | Helper | date-from-now", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks, "de-ch");

  hooks.beforeEach(function () {
    this.date = DateTime.now().minus({ days: 6 });
  });

  test("it renders with a date", async function (assert) {
    this.value = this.date.toJSDate();

    await render(hbs`{{date-from-now this.value}}`);

    assert.dom(this.element).hasText("vor 6 Tagen");
  });

  test("it renders with a string", async function (assert) {
    this.value = this.date.toISO();

    await render(hbs`{{date-from-now this.value}}`);

    assert.dom(this.element).hasText("vor 6 Tagen");
  });
});
