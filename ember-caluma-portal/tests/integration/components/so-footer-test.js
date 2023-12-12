import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | so-footer", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<SoFooter />`);

    assert.dom("footer").exists();
    assert.dom("footer ul li:nth-of-type(1)").hasText(t("nav.faq"));
    assert.dom("footer ul li:nth-of-type(2)").hasText(t("so-footer.contact"));
  });
});
