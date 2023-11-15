import { visit, fillIn, click, waitFor } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";
import setupConfig from "dummy/tests/helpers/config";

module("Acceptance | rejection", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupConfig(hooks);

  hooks.beforeEach(function () {
    this.instanceStates = {
      circulation: this.server.create("instance-state").id,
      rejected: this.server.create("instance-state").id,
    };

    this.config.set("instanceStates", this.instanceStates);
    this.config.set("rejection", {
      instanceState: "rejected",
      allowedInstanceStates: ["circulation"],
    });

    const activeService = this.server.create("public-service");

    this.instance = this.server.create("instance", { activeService });

    this.server.create("case", {
      meta: { "camac-instance-id": this.instance.id },
    });

    const ebauModules = this.owner.lookup("service:ebau-modules");
    ebauModules.serviceId = activeService.id;
    ebauModules.instanceId = this.instance.id;
  });

  test("it can reject instance", async function (assert) {
    this.instance.update({ instanceStateId: this.instanceStates.circulation });

    await visit("/rejection");

    assert.dom("div[data-test-rejection-info]").exists();

    await fillIn("textarea[name=feedback]", "My rejection feedback");
    await click("button[data-test-reject]");

    await waitFor("button[data-test-revert]");

    assert.dom("button[data-test-reject]").doesNotExist();
    assert.dom("textarea[name=feedback]").isDisabled();
  });

  test("it can revert instance rejection", async function (assert) {
    this.instance.update({ instanceStateId: this.instanceStates.rejected });

    await visit("/rejection");

    assert.dom("div[data-test-rejection-info]").exists();
    assert.dom("textarea[name=feedback]").isDisabled();

    await click("button[data-test-revert]");

    await waitFor("button[data-test-reject]");

    assert.dom("button[data-test-revert]").doesNotExist();
    assert.dom("textarea[name=feedback]").isEnabled();
  });
});
