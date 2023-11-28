import {
  click,
  fillIn,
  find,
  focus,
  render,
  tab,
  waitFor,
  waitUntil,
} from "@ember/test-helpers";
import { faker } from "@faker-js/faker";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { selectChoose } from "ember-power-select/test-support";
import { DateTime } from "luxon";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | permissions/create-acl-modal",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);
    setupIntl(hooks, "de");

    hooks.beforeEach(function (assert) {
      // mock needed mirage data
      this.set("instance", this.server.create("instance"));
      this.set("instanceAcl", this.server.create("instance-acl"));
      this.set("publicService", this.server.create("public-service"));
      this.server.create("service", { id: this.publicService.id });

      // setup props and handlers
      this.set("visible", false);
      this.set("onHide", () => {
        assert.step("hide");
        this.set("visible", false);
      });
      this.set("afterCreate", () => assert.step("afterCreate"));
    });

    test("creation of a new instance acl", async function (assert) {
      await render(
        hbs`<Permissions::CreateAclModal 
          @visible={{this.visible}} 
          @instanceId={{this.instance.id}} 
          @onHide={{this.onHide}} 
          @afterCreate={{this.afterCreate}}
        />`,
      );

      assert.dom("[data-test-modal-create-instance-acl]").isNotVisible();
      this.set("visible", true);
      await waitFor("[data-test-modal-create-instance-acl]");

      // fill in form
      await selectChoose(
        "[data-test-acl-service-select]",
        this.publicService.name,
      );
      await selectChoose(
        "[data-test-acl-access-level-select]",
        this.instanceAcl.accessLevel.name,
      );
      // tab into input field to trigger first flatpickr vaux event otherwise manual input won't work
      focus("[data-test-acl-start-time-input] input:not([type=hidden])");
      await tab();
      // manual input
      const today = faker.date.soon();
      await fillIn(
        "[data-test-acl-start-time-input] input:not([type=hidden])",
        `${today.toLocaleDateString("de-CH", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
        })} ${today.toLocaleTimeString().slice(0, 5)}`,
      );
      await tab();
      await click("[data-test-acl-submit]");

      await waitUntil(
        function () {
          return !find("[data-test-modal-create-instance-acl]");
        },
        { timeout: 2000 },
      );

      // assert request
      const requests = this.server.pretender.handledRequests;
      assert.strictEqual(requests[requests.length - 1].method, "POST");
      assert.deepEqual(
        JSON.parse(requests[requests.length - 1].requestBody).data.attributes[
          "start-time"
        ],
        DateTime.fromJSDate(today)
          .set({ second: 0, millisecond: 0 })
          .toUTC()
          .toISO(),
      );
      // verify steps
      assert.verifySteps(["afterCreate", "hide"]);
    });
  },
);
