import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | journal-entry", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    const journal = this.server.create("journal-entry", {
      user: this.server.create("public-user", { name: "John", surname: "Doe" }),
      service: this.server.create("public-service", { name: "ACME Inc." }),
    });

    this.model = (
      await this.owner
        .lookup("service:store")
        .query("journal-entry", { include: "user,service" })
    )[0];

    await render(hbs`<JournalEntry @journalEntry={{this.model}} />`);

    assert.dom("[data-test-creator]").hasText("John Doe (ACME Inc.)");
    assert.dom("[data-test-journal-text]").hasText(journal.text);
  });
});
