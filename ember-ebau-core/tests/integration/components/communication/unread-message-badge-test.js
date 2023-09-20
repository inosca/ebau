import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | communication/unread-message-badge",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    test("it renders count of unread messages", async function (assert) {
      this.server.createList("communications-message", 2);

      await render(hbs`<Communication::UnreadMessageBadge />`);

      assert.dom("[data-test-badge]").exists();
      assert.dom("[data-test-badge]").hasText("2");

      const requests = this.server.pretender.handledRequests;
      assert.deepEqual(requests[requests.length - 1].queryParams, {
        is_read: "false",
        "page[number]": "1",
        "page[size]": "1",
      });
    });
  },
);
