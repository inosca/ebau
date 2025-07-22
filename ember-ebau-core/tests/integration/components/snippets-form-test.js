import { click, fillIn, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";
import { fake } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | snippets-form", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    this.snippet = this.server.create("notification-template");

    await render(hbs`<SnippetsForm />`);

    assert.dom("h2").hasText(t("snippets.new"));

    await render(hbs`<SnippetsForm @id={{this.snippet.id}} />`);

    assert.dom("h2").hasText(t("snippets.edit"));
  });

  test("it can cancel", async function (assert) {
    this.snippet = this.server.create("notification-template", {
      subject: "Test",
    });

    await render(hbs`<SnippetsForm @id={{this.snippet.id}} />`);

    const snippet = this.owner
      .lookup("service:store")
      .peekRecord("notification-template", this.snippet.id);

    assert.strictEqual(snippet.subject, "Test");
    await fillIn("input[name=subject]", "Test new");
    assert.strictEqual(snippet.subject, "Test new");

    const transitionTo = fake();
    this.owner.lookup("service:router").transitionTo = transitionTo;
    this.owner.lookup("service:ebau-modules").resolveModuleRoute = () =>
      "snippets.index";

    await click("[data-test-cancel-edit-snippet]");

    assert.true(transitionTo.called);
    assert.deepEqual(transitionTo.args, [["snippets.index"]]);

    assert.strictEqual(snippet.subject, "Test");
  });
});
