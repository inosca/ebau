import Service from "@ember/service";
import { render, click, fillIn } from "@ember/test-helpers";
import { tracked } from "@glimmer/tracking";
import { setupMirage } from "ember-cli-mirage/test-support";
import { task } from "ember-concurrency";
import { setupIntl } from "ember-intl/test-support";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | be-dashboard", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
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
      class MockService extends Service {
        @tracked isSupport = false;
        @tracked language = "de";

        @task
        *refreshAuthentication() {
          yield true;
        }
      },
    );
  });

  test("it renders readonly", async function (assert) {
    await render(hbs`<BeDashboard class="content" @page="test-content" />`);

    assert.dom(".content h1").hasText("TITLE");
    assert.dom(".content p").hasText("CONTENT");
  });

  test("it can be edited by support users", async function (assert) {
    this.owner.lookup("service:session").set("isSupport", true);

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
