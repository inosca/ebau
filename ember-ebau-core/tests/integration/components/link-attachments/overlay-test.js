import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | link-attachments/overlay", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.selected = false;
    this.attachment = { displayName: "test.pdf", context: {} };

    await render(hbs`
      <LinkAttachments::Overlay
        @attachment={{this.attachment}}
        @selected={{this.selected}}
      />
    `);

    assert
      .dom(".uk-overlay.uk-overlay-primary")
      .doesNotHaveClass("link-attachments__preview__overlay--selected");
    assert.dom(".uk-overlay.uk-overlay-primary > del").doesNotExist();
    assert.dom(".uk-overlay.uk-overlay-primary").hasText("test.pdf");

    this.set("selected", true);

    assert
      .dom(".uk-overlay.uk-overlay-primary")
      .hasClass("link-attachments__preview__overlay--selected");

    this.set("attachment", {
      displayName: "test-replaced.pdf",
      context: { isReplaced: true },
    });

    assert.dom(".uk-overlay.uk-overlay-primary > del").exists();
    assert
      .dom(".uk-overlay.uk-overlay-primary > del")
      .hasText("test-replaced.pdf");
  });
});
