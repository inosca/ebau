import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | history", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.instance = this.server.create("instance");
    this.owner.lookup("service:ebau-modules").instanceId = this.instance.id;
  });

  test("it can list history entires", async function (assert) {
    this.server.createList("history-entry", 5, {
      instanceId: this.instance.id,
    });

    await visit(`/history`);

    assert.dom("tbody > tr").exists({ count: 5 });
  });

  test("it handles empty state", async function (assert) {
    await visit(`/history`);

    assert.dom("tbody > tr").exists({ count: 1 });
    assert.dom("tbody > tr > td").hasText(t("global.empty"));
  });

  test("it can expand and collapse rows", async function (assert) {
    this.server.create("history-entry", {
      instanceId: this.instance.id,
      body: "test",
    });

    await visit(`/history`);

    assert.dom("[data-test-history-body]").doesNotExist();
    await click("[data-test-history-toggle]");
    assert.dom("[data-test-history-body]").hasText("test");
    await click("[data-test-history-toggle]");
    assert.dom("[data-test-history-body]").doesNotExist();
  });
});
