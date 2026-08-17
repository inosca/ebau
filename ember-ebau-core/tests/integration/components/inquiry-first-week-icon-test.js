import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";
import UIkit from "uikit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | inquiry-first-week-icon", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.status = {
      label: "Test!",
      color: "success",
    };

    await render(hbs`<InquiryFirstWeekIcon @status={{this.status}} />`);

    assert.dom("span").hasText("W1");
    assert.dom("span").hasClass("uk-text-success");
    assert.strictEqual(
      UIkit.tooltip(this.element.querySelector("span")).title,
      "Erste Woche: Test!",
    );
  });
});
