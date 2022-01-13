import Service from "@ember/service";
import {
  visit,
  triggerEvent,
  click,
  waitFor,
  currentRouteName,
  currentURL,
} from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

const USER_ID = 1;
const GROUP_ID = 1;

class FakeShoebox extends Service {
  get content() {
    return { userId: USER_ID, groupId: GROUP_ID };
  }
}

module("Acceptance | dossier-import", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({ token: "sometoken" });

    this.server.create("user");
    this.server.create("group");
    this.owner.register("service:shoebox", FakeShoebox);
  });

  test("it can list imports", async function (assert) {
    assert.expect(4);

    const dossierImport = this.server.createList("dossier-import", 5)[0];

    await visit(`/dossier-import`);

    await waitFor("[data-test-imports-row]", { timeout: 2000 });
    assert.dom("[data-test-imports-row]").exists({ count: 5 });

    assert
      .dom(`[data-test-imports-row='${dossierImport.id}']`)
      .includesText(dossierImport.user.surname);
    assert
      .dom(`[data-test-imports-row='${dossierImport.id}']`)
      .includesText(`status.${dossierImport.status}`);

    await click(`[data-test-imports-row='${dossierImport.id}'] a`);
    assert.strictEqual(currentURL(), `/dossier-import/${dossierImport.id}`);
  });

  test("it can upload new zip files", async function (assert) {
    assert.expect(6);

    await visit(`/dossier-import`);
    await click("[data-test-new-import]");

    assert.strictEqual(currentRouteName(), "dossier-import.new");

    assert.dom("[data-test-file-upload-name]").doesNotExist();
    assert.dom("[data-test-detail-link]").doesNotExist();
    await triggerEvent("input[type=file]", "change", {
      files: [new File(["foo"], "foo.zip", { type: "application/zip" })],
    });

    await waitFor("[data-test-file-upload-name]", { timeout: 2000 });
    assert.dom("[data-test-file-upload-name]").hasText("foo.zip");

    this.server.schema.dossierImports.first().destroy();

    await triggerEvent("[data-test-dropzone]", "drop", {
      dataTransfer: {
        files: [new File(["bar"], "bar.zip", { type: "application/zip" })],
      },
    });

    await waitFor("[data-test-file-upload-name]", { timeout: 2000 });
    assert.dom("[data-test-file-upload-name]").hasText("bar.zip");

    await click("[data-test-detail-link]");
    assert.strictEqual(
      currentURL(),
      `/dossier-import/${this.server.schema.dossierImports.first().id}`
    );
  });

  test("it can delete imports", async function (assert) {
    assert.expect(5);
    const dossierImport = this.server.createList("dossier-import", 5)[0];

    await visit(`/dossier-import`);

    await waitFor("[data-test-imports-row]", { timeout: 2000 });
    await click(`[data-test-imports-row='${dossierImport.id}'] a`);

    assert.strictEqual(currentURL(), `/dossier-import/${dossierImport.id}`);
    await waitFor("[data-test-import-detail]");
    assert
      .dom("[data-test-import-detail]")
      .includesText(`${dossierImport.user.surname}`);

    await click("button[data-test-action-button='deleteImport']");

    await waitFor("[data-test-imports-row]", { timeout: 2000 });
    assert.strictEqual(currentRouteName(), "dossier-import.index");
    assert.dom("[data-test-imports-row]").exists({ count: 4 });
    assert.dom(`[data-test-imports-row='${dossierImport.id}'`).doesNotExist();
  });
});
