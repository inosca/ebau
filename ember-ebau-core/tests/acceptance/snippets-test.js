import { visit } from "@ember/test-helpers";
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
});
