import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | snippets-table", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    this.service = this.server.create("service");
    const ebauModules = this.owner.lookup("service:ebau-modules");
    ebauModules.serviceId = this.service.id;

    this.server.create("notification-template", {
      purpose: "A",
      service: this.service,
    });
    this.server.create("notification-template", {
      purpose: "B",
      service: this.service,
    });

    await render(hbs`<SnippetsTable />`);

    assert.dom("table[data-test-snippets-table]").exists({ count: 2 });
  });
});
