import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "camac-ng/tests/helpers";

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

    assert.dom("[data-test-history-body]").doesNotExist();
    await click("[data-test-history-toggle]");
    assert.dom("[data-test-history-body]").hasText("test");
    await click("[data-test-history-toggle]");
    assert.dom("[data-test-history-body]").doesNotExist();
  });
});
