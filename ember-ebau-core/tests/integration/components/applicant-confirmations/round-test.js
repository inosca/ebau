import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | applicant-confirmations/round",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    hooks.beforeEach(async function () {
      const round = this.server.create("applicant-confirmation-round", {
        status: "running",
      });

      this.round = await this.owner
        .lookup("service:store")
        .findRecord("applicant-confirmation-round", round.id, {
          include: "confirmations",
        });
    });

    test("it renders", async function (assert) {
      await render(
        hbs`<ApplicantConfirmations::Round @round={{this.round}} @index={{1}} />`,
      );

      assert.dom("h4").hasText("1. Bestätigungsrunde");
      assert.dom("h4 + span").containsText("Gestartet am");
      assert.dom("span.uk-label-success.uk-label-outline").exists();
      assert.dom("ul.applicant-confirmations").exists();
      assert
        .dom("ul.applicant-confirmations > li[data-test-confirmation]")
        .exists({ count: (await this.round.confirmations).length });
    });
  },
);
