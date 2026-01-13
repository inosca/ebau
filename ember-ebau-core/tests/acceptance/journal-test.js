import { visit, click, fillIn } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | journal", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.instance = this.server.create("instance");
    this.service = this.server.create("public-service");
    this.user = this.server.create("public-user");

    this.owner.lookup("service:ebau-modules").instanceId = this.instance.id;
    this.owner.lookup("service:ebau-modules").serviceId = this.service.id;
    this.owner.lookup("service:ebau-modules").userId = this.user.id;
  });

  test("it can list journal entires", async function (assert) {
    this.server.createList("journal-entry", 5, {
      instanceId: this.instance.id,
    });

    await visit(`/journal`);

    assert.dom(".uk-card").exists({ count: 5 });
  });

  test("it handles empty state", async function (assert) {
    await visit(`/journal`);

    assert.dom("[data-test-journal-list]").hasText(t("global.empty"));
  });

  test("it can create a journal entry", async function (assert) {
    await visit(`/journal`);

    await click("[data-test-create]");
    await fillIn("[data-test-textarea]", "Lorem ipsum");
    await click("[data-test-save]");

    assert.dom(".uk-card").exists({ count: 1 });
    assert.dom("[data-test-journal-text]").hasText("Lorem ipsum");
  });

  test("it can edit a journal entry", async function (assert) {
    this.server.create("journal-entry", {
      instanceId: this.instance.id,
      userId: this.user.id,
      service: this.service,
    });

    await visit(`/journal`);

    await click("[data-test-edit-entry]");
    await fillIn("[data-test-textarea]", "Lorem ipsum");
    await click("[data-test-save]");

    assert.dom(".uk-card").exists({ count: 1 });
    assert.dom("[data-test-journal-text]").hasText("Lorem ipsum");
  });
});
