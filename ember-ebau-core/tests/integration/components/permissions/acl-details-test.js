import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | permissions/acl-details", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.server.create("access-level", {
      slug: "service",
      requiredGrantType: "service",
    });
    this.instance = this.server.create("instance");
  });

  test("it shows details of a instance-acl", async function (assert) {
    this.set(
      "acl",
      this.server.create("instance-acl", {
        instance: this.instance,
      }),
    );

    this.set("onHide", () => (this.acl = undefined));

    await render(
      hbs`<Permissions::AclDetails @instanceAcl={{this.acl}} @onHide={{this.onHide}}/>`,
    );

    assert
      .dom("[data-test-instance-acl-modal-entity-name]")
      .containsText(this.acl.entityName);
    assert
      .dom("[data-test-instance-acl-modal-email]")
      .containsText(this.acl.entityEmail);
    assert
      .dom("[data-test-instance-acl-modal-status]")
      .containsText(
        `${this.intl.t("permissions.details.status")} ${this.intl.t(
          `permissions.status.${this.acl.status}`,
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-access-level]")
      .containsText(
        `${this.intl.t("permissions.details.accessLevel")} ${
          this.acl.accessLevel.name
        }`,
      );
    assert
      .dom("[data-test-instance-acl-modal-created-at]")
      .containsText(
        `${this.intl.t("permissions.details.createdAt")} ${this.intl.formatDate(
          this.acl.createdAt,
          { format: "date" },
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-start-time]")
      .containsText(
        `${this.intl.t("permissions.details.startTime")} ${this.intl.formatDate(
          this.acl.startTime,
          { format: "date" },
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-end-time]")
      .containsText(
        `${this.intl.t("permissions.details.endTime")} ${
          this.acl.endTime
            ? this.intl.formatDate(this.acl.endTime, { format: "date" })
            : "-"
        }`,
      );
    assert
      .dom("[data-test-instance-acl-modal-revoked-by]")
      .containsText(
        `${this.intl.t("permissions.details.revokedBy")}${
          this.acl.revokedByUser
            ? ` ${this.acl.revokedByUser.name} ${this.acl.revokedByUser.surname}`
            : ""
        }`,
      );
  });
});
