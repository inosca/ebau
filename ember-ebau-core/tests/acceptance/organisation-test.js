import { visit, fillIn, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";
import { setupFeatures } from "ember-ebau-core/test-support";

const SERVICE_ID = 1;

const DATA = {
  id: String(SERVICE_ID),
  name: "ACME",
  department: "Foobar",
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
  slug: null,
  logo: null,
  usesEchApi: false,
};

DATA.description = DATA.name;

module("Acceptance | organisation", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupFeatures(hooks);

  hooks.beforeEach(async function () {
    this.features.enable("organisation.department");

    this.owner.lookup("service:ebau-modules").serviceId = SERVICE_ID;

    this.server.create("service", { id: SERVICE_ID, name: DATA.name });
  });

  test("can edit the own organisation", async function (assert) {
    await visit("/service-permissions/organisation");

    await fillIn("input[name=department]", DATA.department);
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

    assert
      .dom(".uk-notification-message.uk-notification-message-success")
      .exists({ count: 1 });
    assert
      .dom(".uk-notification-message.uk-notification-message-success")
      .containsText(t("service-permissions.organisation-save-success"));
  });
});
