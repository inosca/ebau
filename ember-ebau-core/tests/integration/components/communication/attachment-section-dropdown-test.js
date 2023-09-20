import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, todo } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | communication/attachment-section-dropdown",
  function (hooks) {
    setupRenderingTest(hooks);

    todo("it renders", async function () {
      await render(hbs`<Communication::AttachmentSectionDropdown />`);
    });
  },
);
