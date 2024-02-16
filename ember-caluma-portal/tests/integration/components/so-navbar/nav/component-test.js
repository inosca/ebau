import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupFeatures } from "ember-ebau-core/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | so-navbar/nav", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupFeatures(hooks);

  test("it renders", async function (assert) {
    this.features.enable("communications");

    await render(hbs`<SoNavbar::Nav @isAuthenticated={{true}} />`);

    const navItems = [
      t("global.title"),
      t("nav.instances"),
      t("nav.communications"),
      t("nav.public-instance"),
    ];

    navItems.forEach((label, i) => {
      assert.dom(`ul li:nth-of-type(${i + 1})`).containsText(label);
    });
  });
});
