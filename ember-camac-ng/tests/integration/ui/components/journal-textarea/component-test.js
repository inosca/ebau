import { render, click, fillIn } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | journal-textarea", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    const journal = this.server.create("journal-entry");
    this.set("journal", journal);

    await render(
      hbs`<JournalTextarea @journalEntry={{this.journal}} @showJournalEntryDuration={{false}}/>`
    );

    await fillIn("[data-test-textarea]", "Lorem ipsum");
    assert.dom("input[id='journal-duration']").doesNotExist();

    await click("[data-test-save]");
    assert.dom("textarea").hasValue("Lorem ipsum");
  });

  test("it renders duration", async function (assert) {
    const journal = this.server.create("journal-entry");
    this.set("journal", journal);

    await render(
      hbs`<JournalTextarea @journalEntry={{this.journal}} @showJournalEntryDuration={{true}}/>`
    );

    await fillIn("[data-test-textarea]", "Lorem ipsum");
    await fillIn("input[id='journal-duration']", "10:15");

    await click("[data-test-save]");
    assert.dom("textarea").hasValue("Lorem ipsum");
    assert.dom("input[id='journal-duration']").hasValue("10:15");
  });
});
