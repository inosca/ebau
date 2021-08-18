import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import setupMirage from "ember-cli-mirage/test-support/setup-mirage";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | journal-entry", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    const journal = this.server.create("journal-entry");
    this.set("journal", journal);

    await render(hbs`<JournalEntry @journalEntry={{this.journal}}/>`);

    assert.dom(".journal-entry-text").hasText(journal.text);
  });
});
