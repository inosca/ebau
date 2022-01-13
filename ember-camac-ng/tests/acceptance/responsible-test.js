import Service from "@ember/service";
import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { selectChoose } from "ember-power-select/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

const SERVICE_ID = 1;

class FakeShoebox extends Service {
  get content() {
    return { serviceId: SERVICE_ID };
  }
}

module("Acceptance | responsible", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({ token: "sometoken" });

    this.owner.register("service:shoebox", FakeShoebox);

    this.server.create("service", { id: SERVICE_ID });
    this.instance = this.server.create("instance");
  });

  test("it can list responsible entires", async function (assert) {
    this.server.createList("responsible-service", 3, {
      instanceId: this.instance.id,
    });

    await visit(`/instances/${this.instance.id}/responsible`);

    assert.dom("tbody > tr").exists({ count: 3 });
  });

  test("it handles empty state", async function (assert) {
    await visit(`/instances/${this.instance.id}/responsible`);

    assert.dom("tbody > tr").exists({ count: 1 });
    assert.dom("tbody > tr > td").hasText("t:global.empty:()");
  });

  test("it can save a responsible user", async function (assert) {
    const users = this.server.createList("user", 3, { serviceId: SERVICE_ID });

    await visit(`/instances/${this.instance.id}/responsible`);

    await selectChoose(
      "[data-test-responsible-user-select]",
      `${users[1].name} ${users[1].surname}`
    );
    await click("[data-test-save-responsible]");

    assert
      .dom("tbody > tr > td:nth-of-type(2)")
      .hasText(`${users[1].name} ${users[1].surname}`);
  });
});
