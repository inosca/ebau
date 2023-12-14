import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | loading-or-notfound", function (hooks) {
  setupRenderingTest(hooks);

  test("it displays a spinner if loading", async function (assert) {
    await render(hbs`<LoadingOrNotfound @loading={{true}} />`);

    assert.dom(".uk-spinner").exists();
  });

  test("it displays a 404 page if not permitted", async function (assert) {
    await render(hbs`<LoadingOrNotfound @hasPermission={{false}} />`);

    assert.dom("h1").hasText(t("notfound.title"));
    assert.dom("h3").hasText(t("notfound.subtitle"));
    assert.dom("p").hasText(`${t("notfound.link")} ${t("notfound.home")}`);
    assert.dom("p > a").exists();
  });

  test("it displays the content if not loading and permitted", async function (assert) {
    await render(hbs`
      <LoadingOrNotfound @hasPermission={{true}} @loading={{false}}>
        <h1>Test</h1>
      </LoadingOrNotfound>
    `);

    assert.dom("h1").hasText("Test");
  });
});
