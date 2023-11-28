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
    assert.dom("[data-test-instance-acl]").exists({ count: 3 });

    await click("button[data-test-filter-button=all]");

    assert.deepEqual(requests[requests.length - 1].queryParams, {
      "filter[status]": "",
      instance: `${this.instance.id}`,
      "page[number]": "1",
      "page[size]": "20",
    });
    assert.dom("[data-test-instance-acl]").exists({ count: 5 });
  });

  test("it shows details for a clicked instance-acl", async function (assert) {
    const acl = this.server.create("instance-acl", {
      instance: this.instance,
    });

    await render(
      hbs`<Permissions::AclTable @instanceId={{this.instance.id}}/>`,
    );
    await click("[data-test-instance-acl]>td>a");
    await waitFor(".permissions-module-modal-dialog");

    assert
      .dom("[data-test-instance-acl-modal-entity-name]")
      .containsText(acl.entityName);
    assert
      .dom("[data-test-instance-acl-modal-email]")
      .containsText(acl.user.email);
    assert
      .dom("[data-test-instance-acl-modal-status]")
      .containsText(
        `${this.intl.t("permissions.details.status")} ${this.intl.t(
          `permissions.status.${acl.status}`,
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-access-level]")
      .containsText(
        `${this.intl.t("permissions.details.access-level")} ${this.intl.t(
          `permissions.access-level.${acl.accessLevel.slug}`,
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-created-at]")
      .containsText(
        `${this.intl.t(
          "permissions.details.created-at",
        )} ${this.intl.formatDate(acl.createdAt, { format: "date" })}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-start-time]")
      .containsText(
        `${this.intl.t(
          "permissions.details.start-time",
        )} ${this.intl.formatDate(acl.startTime, { format: "date" })}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-end-time]")
      .containsText(
        `${this.intl.t("permissions.details.end-time")} ${
          acl.endTime
            ? this.intl.formatDate(acl.endTime, { format: "date" })
            : "-"
        }`,
      );
    assert
      .dom("[data-test-instance-acl-modal-revoked-by]")
      .containsText(
        `${this.intl.t("permissions.details.revoked-by")}${
          acl.revokedByUser
            ? ` ${acl.revokedByUser.name} ${acl.revokedByUser.surname}`
            : ""
        }`,
      );
  });
});
