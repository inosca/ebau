import Service from "@ember/service";
import { visit, fillIn, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "camac-ng/tests/helpers";

const SERVICE_ID = 1;

const DATA = {
  id: String(SERVICE_ID),
  name: "ACME",
  phone: "+41 79 999 99 99",
  zip: "3000",
  city: "Bern",
  address: "Bahnhofstrasse 33",
  email: "info@acme.com",
  website: "https://acme.com",
  notification: true,
  responsibilityConstructionControl: false,
  disabled: false,
  userIds: null,
  activationIds: null,
  serviceGroupId: null,
  serviceParentId: null,
};

DATA.description = DATA.name;

class FakeShoebox extends Service {
  get content() {
    return { serviceId: SERVICE_ID };
  }
}

module("Acceptance | organisation", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.owner.register("service:shoebox", FakeShoebox);

    this.server.create("service", { id: SERVICE_ID, name: DATA.name });

    await authenticateSession();
  });

  test("can edit the own organisation", async function (assert) {
    await visit("/service-permissions/organisation");

    await fillIn("input[name=phone]", DATA.phone);
    await fillIn("input[name=zip]", DATA.zip);
    await fillIn("input[name=city]", DATA.city);
    await fillIn("input[name=address]", DATA.address);
    await fillIn("input[name=email]", DATA.email);
    await fillIn("input[name=website]", DATA.website);
    await click("input[name=notification]");

    await click("button[type=submit]");

    assert.deepEqual(
      JSON.parse(
        JSON.stringify(this.server.schema.find("service", SERVICE_ID)),
      ),
      DATA,
    );

    assert.dom(".uk-alert.uk-alert-success").exists({ count: 1 });
    assert
      .dom(".uk-alert.uk-alert-success")
      .containsText(t("service-permissions.organisation-save-success"));
  });
});
