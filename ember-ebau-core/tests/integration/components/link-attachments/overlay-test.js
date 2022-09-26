import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | link-attachments/overlay", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`
      <LinkAttachments::Overlay
        @attachment={{this.attachment}}
        @selected={{this.selected}}
      />
    `);

    assert
      .dom(".uk-overlay.uk-overlay-primary")
      .doesNotHaveClass("link-attachments__preview__overlay--selected");

    this.set("selected", true);

    assert
      .dom(".uk-overlay.uk-overlay-primary")
      .hasClass("link-attachments__preview__overlay--selected");
  });
});
