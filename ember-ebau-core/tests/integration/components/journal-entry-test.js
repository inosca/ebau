import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | journal-entry", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    const journal = this.server.create("journal-entry");
    const model = await this.owner
      .lookup("service:store")
      .query("journal-entry", { include: "user" });
    this.set("model", model.toArray()[0]);

    await render(hbs`<JournalEntry @journalEntry={{this.model}}/>`);

    assert.dom("[data-test-journal-text]").hasText(journal.text);
  });
});
