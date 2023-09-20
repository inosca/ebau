import { render, settled, click } from "@ember/test-helpers";
import { getOwnConfig } from "@embroider/macros";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";
import testIf from "caluma-portal/tests/helpers/test-if";

module("Integration | Component | be-navbar", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.before(function () {
    this.setLanguage = async function (language) {
      this.owner.lookup("service:session").set("language", language);
      await settled();
    };

    this.resetLanguage = async function () {
      this.owner.lookup("service:session").set("language", "de");
      await settled();
    };
  });

  hooks.beforeEach(async function () {
    this.server.create("user", { name: "John", surname: "Doe" });
  });

  hooks.afterEach(async function () {
    await this.resetLanguage();
  });

  testIf("be")("it renders the logo dynamically", async function (assert) {
    assert.expect(2);

    await render(hbs`<BeNavbar />`);

    await this.setLanguage("de");
    assert
      .dom(".main-logo-be img")
      .hasAttribute("src", "/assets/images/logo-ebau-bern-1-de.svg");

    await this.setLanguage("fr");
    assert
      .dom(".main-logo-be img")
      .hasAttribute("src", "/assets/images/logo-ebau-bern-1-fr.svg");
  });

  test("it renders the static navigation", async function (assert) {
    const navItems = [
      "t:nav.index:()",
      "t:nav.instances:()",
      ...(getOwnConfig().enableCommunications
        ? ["t:nav.communications:()"]
        : []),
      "t:nav.support:()",
    ];

    await authenticateSession();

    await render(hbs`<BeNavbar />`);

    navItems.forEach((label, i) => {
      assert
        .dom(`.uk-navbar-left ul > li:nth-of-type(${i + 1}) > a`)
        .containsText(label);
    });
  });

  testIf("be")("it renders a language switcher", async function (assert) {
    assert.expect(4);

    await render(hbs`<BeNavbar />`);

    assert.dom(".uk-navbar-right ul > li:nth-of-type(1) > a").hasText("de");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(2) > a").hasText("fr");

    await this.setLanguage("de");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(1)").hasClass("uk-active");
    await click(".uk-navbar-right ul > li:nth-of-type(2) > a");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(2)").hasClass("uk-active");
  });
});
