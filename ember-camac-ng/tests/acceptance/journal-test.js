import { visit, click, fillIn } from "@ember/test-helpers";
import setupMirage from "ember-cli-mirage/test-support/setup-mirage";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Acceptance | journal", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({ token: "sometoken" });

    this.instance = this.server.create("instance");
  });

  test("it can list journal entires", async function (assert) {
    this.server.createList("journal-entry", 5, {
      instanceId: this.instance.id,
    });

    await visit(`/instances/${this.instance.id}/journal`);

    assert.dom("article").exists({ count: 5 });
  });

  test("it handles empty state", async function (assert) {
    await visit(`/instances/${this.instance.id}/journal`);

    assert.dom("[data-test-journal-list]").hasText("t:global.empty:()");
  });

  test("it can create a journal entry", async function (assert) {
    await visit(`/instances/${this.instance.id}/journal`);

    await click("[data-test-create]");
    await fillIn("[data-test-textarea]", "Lorem ipsum");
    await click("[data-test-save]");

    assert.dom("article").exists({ count: 1 });
    assert.dom(".uk-comment-body").hasText("Lorem ipsum");
  });

  test("it can edit a journal entry", async function (assert) {
    this.server.create("journal-entry", {
      instanceId: this.instance.id,
    });

    await visit(`/instances/${this.instance.id}/journal`);

    await click("[data-test-edit-entry]");
    await fillIn(".uk-comment [data-test-textarea]", "Lorem ipsum");
    await click(".uk-comment [data-test-save]");

    assert.dom("article").exists({ count: 1 });
    assert.dom(".uk-comment-body").hasText("Lorem ipsum");
  });
});
