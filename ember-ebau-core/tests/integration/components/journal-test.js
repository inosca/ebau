import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | journal", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<Journal @instanceId={{2}}/>`);

    assert
      .dom(this.element)
      .hasText(`${t("journal.create")} ${t("global.empty")}`);
  });
});
