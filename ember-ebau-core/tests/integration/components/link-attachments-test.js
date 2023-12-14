import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | link-attachments", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    const instance = this.server.create("instance");
    const section = this.server.create("attachment-section");
    const attachments = this.server.createList("attachment", 5, {
      attachmentSectionIds: [section.id],
      instance,
    });

    this.field = {
      answer: { value: attachments.slice(0, 2).map((a) => a.id) },
      question: { raw: { meta: { attachmentSection: 1 } } },
    };
    this.context = { instanceId: instance.id };

    await render(hbs`
      <LinkAttachments
        @field={{this.field}}
        @context={{this.context}}
      />
    `);

    assert.dom(".link-attachments__preview").exists({ count: 2 });
    assert.dom(".link-attachments__preview").hasText(attachments[0].name);
  });
});
