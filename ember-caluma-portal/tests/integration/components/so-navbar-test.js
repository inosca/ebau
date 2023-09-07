import { render } from "@ember/test-helpers";
import { getOwnConfig } from "@embroider/macros";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | so-navbar", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.server.create("user", { name: "John", surname: "Doe" });
    await authenticateSession();
  });

  test("it renders", async function (assert) {
    await render(hbs`<SoNavbar />`);

    const navItems = [
      "t:global.title:()",
      "t:nav.instances:()",
      ...(getOwnConfig().enableCommunications
        ? ["t:nav.communications:() 3"]
        : []),
      "t:nav.public-instance:()",
    ];

    assert.dom("header").exists();
    assert.dom("nav").exists();

    // nav left
    navItems.forEach((label, i) => {
      assert
        .dom(`nav div:nth-of-type(1) ul li:nth-of-type(${i + 1})`)
        .hasText(label);
    });

    // nav right
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(1)")
      .hasText("t:so-footer.leave:()");
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(2) svg.fa-circle-question")
      .exists();
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(3)")
      .hasText("John Doe t:nav.logout:()");
    assert
      .dom("nav div:nth-of-type(2) ul li:nth-of-type(4) svg.fa-power-off")
      .exists();
  });
});
