import { currentURL, fillIn, visit } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | snippets", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  test("list snippets", async function (assert) {
    this.server.createList("notification-template", 3, {
      purpose: "A category",
    });

    await visit("/snippets");

    assert
      .dom('table[data-test-snippets-table="A category"] tbody tr')
      .exists({ count: 3 });
    assert.dom("[data-test-copy-snippet]").exists({ count: 3 });
  });

  test("search snippets", async function (assert) {
    this.server.createList("notification-template", 2);

    await visit("/snippets");
    await fillIn("[data-test-search]", "Test");

    assert.strictEqual(currentURL(), "/snippets?search=Test");

    const requests = this.server.pretender.handledRequests;

    assert.strictEqual(requests.length, 2);
    assert.strictEqual(
      requests[0].url,
      "/api/v1/notification-templates?search=&type=textcomponent",
    );
    assert.strictEqual(
      requests[1].url,
      "/api/v1/notification-templates?search=Test&type=textcomponent",
    );
  });
});
