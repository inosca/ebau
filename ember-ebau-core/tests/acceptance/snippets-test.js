import { currentURL, fillIn, visit } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | snippets", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  hooks.beforeEach(async function () {
    this.user = this.server.create("public-user");
    this.service = this.server.create("service");
    const ebauModules = this.owner.lookup("service:ebau-modules");
    ebauModules.serviceId = this.service.id;
  });

  test("list snippets", async function (assert) {
    this.server.createList("notification-template", 3, {
      purpose: "A category",
      type: "textcomponent",
      service: this.service,
    });

    await visit("/snippets");

    assert
      .dom('table[data-test-snippets-table="A category"] tbody tr')
      .exists({ count: 3 });
    assert.dom("[data-test-copy-snippet]").exists({ count: 3 });
  });

  test("search snippets", async function (assert) {
    this.server.createList("notification-template", 2, {
      type: "textcomponent",
      service: this.service,
    });

    await visit("/snippets");
    await fillIn("[data-test-search]", "Test");

    assert.strictEqual(currentURL(), "/snippets?search=Test");

    const requests = this.server.pretender.handledRequests;

    assert.strictEqual(requests.length, 3);
    assert.strictEqual(
      requests[0].url,
      "/api/v1/notification-templates?search=&type=textcomponent",
    );
    assert.strictEqual(
      requests[2].url,
      "/api/v1/notification-templates?search=Test&type=textcomponent",
    );
  });
});
