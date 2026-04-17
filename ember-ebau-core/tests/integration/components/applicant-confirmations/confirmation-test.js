import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | applicant-confirmations/confirmation",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    test("it renders with user", async function (assert) {
      const model = this.server.create("applicant-confirmation", {
        status: "confirmed",
      });
      this.model = await this.owner
        .lookup("service:store")
        .findRecord("applicant-confirmation", model.id);

      await render(
        hbs`<ApplicantConfirmations::Confirmation @confirmation={{this.model}} />`,
      );

      assert.dom(`li[data-test-confirmation="${this.model.id}"]`).exists();
      assert
        .dom(".applicant-confirmations__item__status")
        .hasClass("uk-text-success");
      assert
        .dom(".applicant-confirmations__item__status > svg")
        .hasAttribute("data-icon", "circle-check");
      assert
        .dom("[data-test-confirmation-user]")
        .containsText(this.model.displayName);
      assert
        .dom("[data-test-confirmation-user]")
        .containsText(this.model.roles.join(", "));
      assert
        .dom("[data-test-confirmation-closed-at]")
        .containsText("bestätigt am");
    });

    test("it renders without user", async function (assert) {
      const model = this.server.create("applicant-confirmation", {
        user: null,
        status: "pending",
      });
      this.model = await this.owner
        .lookup("service:store")
        .findRecord("applicant-confirmation", model.id);

      await render(
        hbs`<ApplicantConfirmations::Confirmation @confirmation={{this.model}} />`,
      );

      assert.dom(`li[data-test-confirmation="${this.model.id}"]`).exists();
      assert
        .dom(".applicant-confirmations__item__status")
        .hasClass("uk-text-muted");
      assert
        .dom(".applicant-confirmations__item__status > svg")
        .hasAttribute("data-icon", "clock");
      assert
        .dom("[data-test-confirmation-user]")
        .containsText(this.model.displayName);
      assert
        .dom("[data-test-confirmation-user]")
        .containsText(this.model.roles.join(", "));
      assert.dom("[data-test-confirmation-user-warning]").exists();
      assert.dom("[data-test-confirmation-closed-at]").doesNotExist();
    });
  },
);
