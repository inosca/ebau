import { render, settled, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

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
      this.owner.lookup("service:session").set("data.language", undefined);
      await settled();
      this.intl.setLocale();
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
      .dom(".be-logo img")
      .hasAttribute("src", "/assets/images/logo-ebau-bern-1-de.svg");

    await this.setLanguage("fr");
    assert
      .dom(".be-logo img")
      .hasAttribute("src", "/assets/images/logo-ebau-bern-1-fr.svg");
  });

  test("it renders the static navigation", async function (assert) {
    assert.expect(3);

    await authenticateSession();

    await render(hbs`<BeNavbar />`);

    assert
      .dom(".uk-navbar-left ul > li:nth-of-type(1) > a")
      .hasText("t:nav.index:()");
    assert
      .dom(".uk-navbar-left ul > li:nth-of-type(2) > a")
      .hasText("t:nav.instances:()");
    assert
      .dom(".uk-navbar-left ul > li:nth-of-type(3) > a")
      .hasText("t:nav.support:()");
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
