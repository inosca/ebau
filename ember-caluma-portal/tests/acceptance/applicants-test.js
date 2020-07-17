import { visit, fillIn, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Acceptance | applicants", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    // camac data
    const user = this.server.create("user");
    const instance = this.server.create("instance", {
      calumaForm: "main-form",
    });

    this.server.create("applicant", { instance });
    this.server.create("applicant", { instance, invitee: user });

    // caluma data
    this.server.create("case", {
      document: this.server.create("document", {
        form: this.server.create("form", {
          slug: "main-form",
          meta: { "is-main-form": true },
        }),
      }),
    });

    await authenticateSession({ access_token: "123qweasdyxc" });

    await visit(`/instances/${instance.id}/applicants`);
  });

  test("can list applicants", async function (assert) {
    assert.expect(1);

    assert.dom("tbody tr").exists({ count: 2 });
  });

  test("can add an applicant", async function (assert) {
    assert.expect(2);

    assert.dom("tbody tr").exists({ count: 2 });

    await fillIn("input[name=email]", "test@example.com");
    await click("button[type=submit]");

    assert.dom("tbody tr").exists({ count: 3 });
  });

  test("can delete an applicant", async function (assert) {
    assert.expect(4);

    assert.dom("tbody tr").exists({ count: 2 });
    assert.dom("tbody tr button").exists({ count: 2 });

    await click("tbody tr:last-of-type button");

    assert.dom("tbody tr").exists({ count: 1 });
    assert.dom("tbody tr button").doesNotExist();
  });
});
