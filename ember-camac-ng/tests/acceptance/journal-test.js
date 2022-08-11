import Service from "@ember/service";
import { visit, click, fillIn } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

const USER_ID = 1;

class FakeShoebox extends Service {
  get content() {
    return { userId: USER_ID };
  }
}

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

    assert.dom(".uk-card").exists({ count: 5 });
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

    assert.dom(".uk-card").exists({ count: 1 });
    assert.dom("[data-test-journal-text]").hasText("Lorem ipsum");
  });

  test("it can edit a journal entry", async function (assert) {
    this.owner.register("service:shoebox", FakeShoebox);

    this.server.create("journal-entry", {
      instanceId: this.instance.id,
      userId: USER_ID,
    });

    await visit(`/instances/${this.instance.id}/journal`);

    await click("[data-test-edit-entry]");
    await fillIn("[data-test-textarea]", "Lorem ipsum");
    await click("[data-test-save]");

    assert.dom(".uk-card").exists({ count: 1 });
    assert.dom("[data-test-journal-text]").hasText("Lorem ipsum");
  });
});
