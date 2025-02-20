import { visit, fillIn, currentURL, click, waitFor } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | snippets-admin", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  test("list snippets", async function (assert) {
    this.server.createList("notification-template", 3, {
      purpose: "A category",
    });
    this.server.createList("notification-template", 5, {
      purpose: "B category",
    });

    await visit("/snippets-admin");

    assert
      .dom('table[data-test-snippets-table="A category"] tbody tr')
      .exists({ count: 4 });
    assert
      .dom('table[data-test-snippets-table="B category"] tbody tr')
      .exists({ count: 6 });
  });

  test("search snippets", async function (assert) {
    this.server.createList("notification-template", 2);

    await visit("/snippets-admin");
    await fillIn("[data-test-search]", "Test");

    assert.strictEqual(currentURL(), "/snippets-admin?search=Test");

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

  test("create new snippet", async function (assert) {
    this.server.create("notification-template", { purpose: "Test" });

    await visit("/snippets-admin");

    assert
      .dom('table[data-test-snippets-table="Test"] tbody tr')
      .exists({ count: 2 });

    await click("[data-test-add-snippet]");

    assert.strictEqual(currentURL(), "/snippets-admin/new?category=Test");

    assert.dom("input[name=purpose]").doesNotExist();
    await fillIn("input[name=subject]", "Subject");
    await fillIn("textarea[name=body]", "Body");

    await click("[data-test-save-snippet]");

    assert.strictEqual(currentURL(), "/snippets-admin");
    assert
      .dom('table[data-test-snippets-table="Test"] tbody tr')
      .exists({ count: 3 });
  });

  test("edit snippet", async function (assert) {
    const snippet = this.server.create("notification-template");

    await visit("/snippets-admin");

    await click(`[data-test-edit-snippet="${snippet.id}"]`);

    assert.strictEqual(currentURL(), `/snippets-admin/${snippet.id}`);

    await fillIn("input[name=subject]", "My new subject!");
    await fillIn("textarea[name=body]", "My new body!");

    await click("[data-test-save-snippet]");

    assert.strictEqual(currentURL(), "/snippets-admin");
    assert
      .dom(
        "table[data-test-snippets-table] tbody tr:first-child td:nth-child(1)",
      )
      .hasText("My new subject!");
    assert
      .dom(
        "table[data-test-snippets-table] tbody tr:first-child td:nth-child(2)",
      )
      .hasText("My new body!");
  });

  test("delete snippet", async function (assert) {
    const snippets = this.server.createList("notification-template", 2, {
      purpose: "A category",
    });
    const snippet = snippets[0];

    await visit("/snippets-admin");

    assert
      .dom('table[data-test-snippets-table="A category"] tbody tr')
      .exists({ count: 3 });

    await click(`[data-test-delete-snippet="${snippet.id}"]`);
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    assert
      .dom('table[data-test-snippets-table="A category"] tbody tr')
      .exists({ count: 2 });
  });

  test("create new category", async function (assert) {
    await visit("/snippets-admin");

    await click("[data-test-new-category]");

    assert.strictEqual(currentURL(), "/snippets-admin/new");

    await fillIn("input[name=purpose]", "My new category");
    await fillIn("input[name=subject]", "My new snippet");
    await fillIn("textarea[name=body]", "Test body");

    await click("[data-test-save-snippet]");

    assert.strictEqual(currentURL(), "/snippets-admin");

    assert.dom('table[data-test-snippets-table="My new category"]').exists();
    assert
      .dom('table[data-test-snippets-table="My new category"] tbody tr')
      .exists({ count: 2 });
  });

  test("edit category", async function (assert) {
    this.server.createList("notification-template", 3, {
      purpose: "Category old",
    });

    await visit("/snippets-admin");

    await click('[data-test-edit-category="Category old"]');
    await fillIn("input[name=purpose]", "Category new");
    await click("[data-test-save-category]");

    // Wait until refresh is done
    await waitFor('table[data-test-snippets-table="Category old"]', {
      count: 0,
    });

    assert.dom('table[data-test-snippets-table="Category old"]').doesNotExist();
    assert.dom('table[data-test-snippets-table="Category new"]').exists();
  });

  test("delete category", async function (assert) {
    this.server.createList("notification-template", 3, {
      purpose: "A category",
    });
    this.server.createList("notification-template", 5, {
      purpose: "B category",
    });

    await visit("/snippets-admin");

    assert.dom('table[data-test-snippets-table="A category"]').exists();
    assert.dom('table[data-test-snippets-table="B category"]').exists();

    await click('[data-test-delete-category="A category"]');
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    // Wait until refresh is done
    await waitFor('table[data-test-snippets-table="A category"]', { count: 0 });

    assert.dom('table[data-test-snippets-table="A category"]').doesNotExist();
    assert.dom('table[data-test-snippets-table="B category"]').exists();
  });
});
