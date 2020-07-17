import Service from "@ember/service";
import { render, settled, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

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

    this.owner.register(
      "service:router",
      Service.extend({
        // eslint-disable-next-line ember/avoid-leaking-state-in-ember-objects
        currentRoute: { name: "dummy", parent: null, params: {} },
      })
    );
  });

  hooks.afterEach(async function () {
    await this.resetLanguage();
  });

  test("it renders the logo dynamically", async function (assert) {
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

  test("it renders a language switcher", async function (assert) {
    assert.expect(4);

    await render(hbs`<BeNavbar />`);

    assert.dom(".uk-navbar-right ul > li:nth-of-type(2) > a").hasText("de");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(3) > a").hasText("fr");

    await this.setLanguage("de");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(2)").hasClass("uk-active");
    await click(".uk-navbar-right ul > li:nth-of-type(3) > a");
    assert.dom(".uk-navbar-right ul > li:nth-of-type(3)").hasClass("uk-active");
  });

  test("it renders a group switcher", async function (assert) {
    assert.expect(4);

    this.server.create("public-group", { name: "Test Group" });

    await render(hbs`<BeNavbar />`);

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John");

    await click(".uk-navbar-right ul > li:nth-of-type(1) > a");

    assert.dom(".uk-dropdown ul > li.uk-active").hasText("t:nav.applicant:()");

    await click(".uk-dropdown ul > li:nth-of-type(3) > a");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John (Test Group)");

    await click(".uk-dropdown ul > li:nth-of-type(1) > a");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John");
  });

  test("it renders a link to the internal section", async function (assert) {
    assert.expect(3);

    const { id: groupId } = this.server.create("public-group");
    const editRoute = {
      name: "instances.edit",
      parent: null,
      params: { instance: 1 },
    };

    this.owner.lookup("service:session").set("group", groupId);

    await render(hbs`<BeNavbar />`);

    assert
      .dom("a.be-navbar-internal-link")
      .hasAttribute("href", "http://camac-ng.local");

    this.owner.lookup("service:router").set("currentRoute", editRoute);
    await settled();

    assert
      .dom("a.be-navbar-internal-link")
      .hasAttribute(
        "href",
        "http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1"
      );

    this.owner.lookup("service:router").set("currentRoute", {
      name: "instances.edit.form",
      parent: editRoute,
      params: { form: "baugesuch" },
    });
    await settled();

    assert
      .dom("a.be-navbar-internal-link")
      .hasAttribute(
        "href",
        "http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1"
      );
  });
});
