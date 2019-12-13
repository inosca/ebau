import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, settled, click } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import { setupIntl } from "ember-intl/test-support";
import { setupMirage } from "ember-cli-mirage/test-support";

module("Integration | Component | navbar", function(hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.before(function() {
    this.setLanguage = async function(language) {
      this.owner.lookup("service:session").set("language", language);
      await settled();
    };

    this.resetLanguage = async function() {
      this.owner.lookup("service:session").set("data.language", undefined);
      await settled();
      this.intl.setLocale();
    };
  });

  hooks.beforeEach(async function() {
    this.server.create("user", { name: "John", surname: "Doe" });
  });

  hooks.afterEach(async function() {
    await this.resetLanguage();
  });

  test("it renders the logo dynamically", async function(assert) {
    assert.expect(2);

    await render(hbs`<Navbar />`);

    await this.setLanguage("de");
    assert
      .dom(".uk-logo img")
      .hasAttribute("src", "/assets/images/logo-ebau-bern-1-de.svg");

    await this.setLanguage("fr");
    assert
      .dom(".uk-logo img")
      .hasAttribute("src", "/assets/images/logo-ebau-bern-1-fr.svg");
  });

  test("it renders the static navigation", async function(assert) {
    assert.expect(3);

    await render(hbs`<Navbar />`);

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

  test("it renders a language switcher", async function(assert) {
    assert.expect(4);

    await render(hbs`<Navbar />`);

    assert.dom(".uk-navbar-right ul > li:nth-of-type(2) > a").hasText("de");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(3) > a").hasText("fr");

    await this.setLanguage("de");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(2)").hasClass("uk-active");
    await click(".uk-navbar-right ul > li:nth-of-type(3) > a");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(3)").hasClass("uk-active");
  });

  test("it renders a group switcher", async function(assert) {
    assert.expect(4);

    this.server.create("group", { name: "Test Group" });

    await render(hbs`<Navbar />`);

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John");

    await click(".uk-navbar-right ul > li:nth-of-type(1) > a");

    assert
      .dom(".uk-navbar-dropdown ul > li.uk-active")
      .hasText("t:nav.applicant:()");

    await click(".uk-navbar-dropdown ul > li:nth-of-type(3) > a");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John (Test Group)");

    await click(".uk-navbar-dropdown ul > li:nth-of-type(1) > a");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John");
  });

  test("it renders meta informations about the application", async function(assert) {
    assert.expect(1);

    await render(hbs`<Navbar />`);

    assert.dom(".uk-navbar-center .uk-label:nth-of-type(2)").hasText("test");
  });
});
