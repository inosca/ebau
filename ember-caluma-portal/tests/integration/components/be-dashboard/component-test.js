import Service from "@ember/service";
import { render, click, fillIn } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

import config from "../../../../config/environment";

module("Integration | Component | be-dashboard", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(function () {
    const question = this.server.create("question", {
      slug: "test-content-de",
      type: "TEXT",
    });

    this.server.create("document", {
      form: this.server.create("form", {
        slug: "dashboard",
        questions: [question],
      }),
      answers: [
        this.server.create("answer", {
          question,
          value: "# TITLE\n\nCONTENT",
        }),
      ],
    });

    this.owner.register(
      "service:session",
      Service.extend({
        group: null,
        language: "de",
      })
    );
  });

  test("it renders readonly", async function (assert) {
    assert.expect(2);

    await render(hbs`<BeDashboard class="content" @page="test-content" />`);

    assert.dom(".content h1").hasText("TITLE");
    assert.dom(".content p").hasText("CONTENT");
  });

  test("it can be edited by support users", async function (assert) {
    assert.expect(5);

    this.owner
      .lookup("service:session")
      .set("group", config.ebau.supportGroups[0]);

    await render(hbs`<BeDashboard class="content" @page="test-content" />`);

    // start editing
    await click("[data-test-dashboard-edit]");
    assert.dom("textarea").hasValue("# TITLE\n\nCONTENT");

    // fill in and cancel
    await fillIn("textarea", "**BOLD**");
    await click("[data-test-dashboard-cancel]");

    assert.dom(".content h1").hasText("TITLE");
    assert.dom(".content p").hasText("CONTENT");

    // start again
    await click("[data-test-dashboard-edit]");
    assert.dom("textarea").hasValue("# TITLE\n\nCONTENT");

    // fill in and save
    await fillIn("textarea", "**BOLD**");
    await click("[data-test-dashboard-save]");

    assert.dom(".content strong").hasText("BOLD");
  });
});
