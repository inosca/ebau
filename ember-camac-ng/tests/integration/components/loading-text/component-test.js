import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | loading-text", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<LoadingText />`);

    assert.dom("span").hasText(`${t("global.loading")}.`);
  });
});
