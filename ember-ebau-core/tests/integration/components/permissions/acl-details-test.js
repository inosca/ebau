import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
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
    const aclId = this.server.create("instance-acl", {
      instance: this.instance,
    }).id;

    this.acl = await this.owner
      .lookup("service:store")
      .findRecord("instance-acl", aclId, {
        include: "access_level",
      });

    this.onHide = () => (this.acl = undefined);

    await render(
      hbs`<Permissions::AclDetails @instanceAcl={{this.acl}} @onHide={{this.onHide}} />`,
    );

    const intl = this.owner.lookup("service:intl");

    assert
      .dom("[data-test-instance-acl-modal-entity-name]")
      .containsText(this.acl.entityName);
    assert
      .dom("[data-test-instance-acl-modal-email]")
      .containsText(this.acl.entityEmail);
    assert
      .dom("[data-test-instance-acl-modal-status]")
      .containsText(
        `${t("permissions.details.status")} ${t(
          `permissions.status.${this.acl.status}`,
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-access-level]")
      .containsText(
        `${t("permissions.details.accessLevel")} ${this.acl.get(
          "accessLevel.name",
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-created-at]")
      .containsText(
        `${t("permissions.details.createdAt")} ${intl.formatDate(
          this.acl.createdAt,
          { format: "date" },
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-start-time]")
      .containsText(
        `${t("permissions.details.startTime")} ${intl.formatDate(
          this.acl.startTime,
          { format: "date" },
        )}`,
      );
    assert
      .dom("[data-test-instance-acl-modal-end-time]")
      .containsText(
        `${t("permissions.details.endTime")} ${
          this.acl.endTime
            ? intl.formatDate(this.acl.endTime, { format: "date" })
            : "-"
        }`,
      );
    assert
      .dom("[data-test-instance-acl-modal-revoked-by]")
      .containsText(
        `${t("permissions.details.revokedBy")} ${
          this.acl.get("revokedByUser.id")
            ? this.acl.get("revokedByUser.fullName")
            : ""
        }`,
      );
  });
});
