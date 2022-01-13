import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Acceptance | history", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({ token: "sometoken" });

    this.instance = this.server.create("instance");
  });

  test("it can list history entires", async function (assert) {
    this.server.createList("history-entry", 5, {
      instanceId: this.instance.id,
    });

    await visit(`/instances/${this.instance.id}/history`);

    assert.dom("tbody > tr").exists({ count: 5 });
  });

  test("it handles empty state", async function (assert) {
    await visit(`/instances/${this.instance.id}/history`);

    assert.dom("tbody > tr").exists({ count: 1 });
    assert.dom("tbody > tr > td").hasText("t:global.empty:()");
  });

  test("it can expand and collapse rows", async function (assert) {
    this.server.create("history-entry", {
      instanceId: this.instance.id,
      body: "test",
    });

    await visit(`/instances/${this.instance.id}/history`);

    assert.dom(".history__row__body").doesNotExist();
    await click(".history__row__toggle__button");
    assert.dom(".history__row__body").hasText("test");
    await click(".history__row__toggle__button");
    assert.dom(".history__row__body").doesNotExist();
  });
});
