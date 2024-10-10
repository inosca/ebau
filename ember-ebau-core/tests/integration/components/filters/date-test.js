import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setFlatpickrDate } from "ember-flatpickr/test-support/helpers";
import { DateTime } from "luxon";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | filters/date", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function (assert) {
    this.nowJS = DateTime.now().toJSDate();
    this.onUpdate = () => {
      assert.step("update");
    };
  });

  test("it renders", async function (assert) {
    await render(hbs`<Filters::Date
  @placeholder="some placeholder"
  @filterName="date-update"
  @label="My Datefilter"
  @hint="date-filter-test-hint"
/>`);

    assert.dom("label").hasText("My Datefilter");
    assert
      .dom("[data-test-filters-date-hint]")
      .hasText("date-filter-test-hint");
    assert
      .dom("[data-test-filters-date-component] input")
      .hasAttribute("placeholder", "some placeholder");
  });

  test("it updates on change", async function (assert) {
    await render(hbs`<Filters::Date
  @value={{this.nowJS}}
  @filterName="date-update"
  @hint="date-filter-test-hint"
  @updateFilter={{this.onUpdate}}
/>`);

    assert
      .dom("[data-test-filters-date-component] input")
      .hasAttribute("value", this.nowJS.toISOString().slice(0, 10));
    setFlatpickrDate("#filter__date__date-update", this.nowJS, true);

    assert.verifySteps(["update"]);
  });
});
