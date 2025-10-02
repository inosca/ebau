import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { selectChoose } from "ember-power-select/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | responsible", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.service = this.server.create("service");
    this.instance = this.server.create("instance");

    const ebauModules = this.owner.lookup("service:ebau-modules");
    ebauModules.serviceId = this.service.id;
    ebauModules.instanceId = this.instance.id;
  });

  test("it can list responsible entires", async function (assert) {
    this.server.createList("responsible-service", 3, {
      instanceId: this.instance.id,
    });

    await visit(`/responsible`);

    assert.dom("tbody > tr").exists({ count: 3 });
  });

  test("it handles empty state", async function (assert) {
    await visit(`/responsible`);

    assert.dom("tbody > tr").exists({ count: 1 });
    assert.dom("tbody > tr > td").hasText(t("global.empty"));
  });

  test("it can save a responsible user", async function (assert) {
    const users = this.server.createList("user", 3, {
      serviceId: this.service.id,
    });

    await visit(`/responsible`);

    await selectChoose(
      "[data-test-responsible-user-select]",
      `${users[1].name} ${users[1].surname}`,
    );
    await click("[data-test-save-responsible]");

    assert
      .dom("tbody > tr > td:nth-of-type(2)")
      .hasText(`${users[1].name} ${users[1].surname}`);
  });
});
