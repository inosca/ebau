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

    await render(hbs`<JournalTextarea @journalEntry={{this.journal}}/>`);

    await fillIn("[data-test-textarea]", "Lorem ipsum");
    await click("[data-test-save]");
    assert.dom("textarea").hasValue("Lorem ipsum");
  });
});
