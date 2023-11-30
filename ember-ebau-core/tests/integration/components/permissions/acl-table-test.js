import { click, render, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | permissions/acl-table", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  hooks.beforeEach(function () {
    this.server.create("access-level", {
      slug: "service",
      name: "Service",
      requiredGrantType: "service",
    });
    this.instance = this.server.create("instance");
  });

  test("it toggles between all, active, scheduled and expired", async function (assert) {
    this.server.createList("instance-acl", 2, "active", {
      instance: this.instance,
    });
    this.server.createList("instance-acl", 3, "expired", {
      instance: this.instance,
    });
    this.server.createList("instance-acl", 1, "scheduled", {
      instance: this.instance,
    });

    await render(
      hbs`<Permissions::AclTable @instanceId={{this.instance.id}}/>`,
    );

    await click("button[data-test-filter-button=active]");

    const requests = this.server.pretender.handledRequests;

    assert.deepEqual(requests[requests.length - 1].queryParams, {
      "filter[status]": "active",
      instance: `${this.instance.id}`,
      "page[number]": "1",
      "page[size]": "20",
    });

    assert.dom("[data-test-instance-acl]").exists({ count: 2 });

    await click("button[data-test-filter-button=scheduled]");

    assert.deepEqual(requests[requests.length - 1].queryParams, {
      "filter[status]": "scheduled",
      instance: `${this.instance.id}`,
      "page[number]": "1",
      "page[size]": "20",
    });
    assert.dom("[data-test-instance-acl]").exists({ count: 1 });

    await click("button[data-test-filter-button=expired]");

    assert.deepEqual(requests[requests.length - 1].queryParams, {
      "filter[status]": "expired",
      instance: `${this.instance.id}`,
      "page[number]": "1",
      "page[size]": "20",
    });
    assert.dom("[data-test-instance-acl]").exists({ count: 3 });

    await click("button[data-test-filter-button=all]");

    assert.deepEqual(requests[requests.length - 1].queryParams, {
      instance: `${this.instance.id}`,
      "page[number]": "1",
      "page[size]": "20",
    });
    assert.dom("[data-test-instance-acl]").exists({ count: 6 });
  });

  test("it shows details for a clicked instance-acl", async function (assert) {
    this.server.create("instance-acl", {
      instance: this.instance,
    });

    await render(
      hbs`<Permissions::AclTable @instanceId={{this.instance.id}}/>`,
    );
    await click("[data-test-instance-acl]>td>a");
    await waitFor(".permissions-module-modal-dialog");

    assert.dom(".permissions-module-modal-dialog").isVisible();
  });
});
