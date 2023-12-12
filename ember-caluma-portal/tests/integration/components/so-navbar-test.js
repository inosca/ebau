import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | so-navbar", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.server.create("user", { name: "John", surname: "Doe" });
    await authenticateSession();
  });

  test("it renders", async function (assert) {
    await render(hbs`<SoNavbar />`);

    assert.dom("header").exists();
    assert.dom("nav").exists();

    // nav right
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(1)")
      .hasText(t("so-footer.leave"));
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(2) svg.fa-circle-question")
      .exists();
    assert
      .dom(
        "nav div:nth-of-type(2) ul li:nth-of-type(3) > a > div:nth-of-type(2)",
      )
      .hasText("John Doe");
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(4) svg.fa-power-off")
      .exists();
  });
});
