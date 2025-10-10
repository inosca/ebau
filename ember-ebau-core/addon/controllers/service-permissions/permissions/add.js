import Controller from "@ember/controller";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { query } from "ember-data-resources";
import { confirm } from "ember-uikit";

import parseError from "ember-ebau-core/utils/parse-error";

export default class ServicePermissionsPermissionsAddController extends Controller {
  @service store;
  @service intl;
  @service router;
  @service ebauModules;
  @service notification;
  @service session;

  @tracked email;
  @tracked group;

  groups = query(this, "group", () => ({
    service_or_subservice: this.ebauModules.serviceId,
  }));

  async invite() {
    if (
      !(await confirm(
        this.intl.t("service-permissions.invitation-modal-body", {
          email: this.email,
        }),
        {
          i18n: {
            ok: this.intl.t("service-permissions.invitation-invite-user"),
            cancel: this.intl.t("global.close"),
          },
        },
      ))
    ) {
      return;
    }

    const userGroupInvitation = this.store.createRecord(
      "user-group-invitation",
      {
        email: this.email,
        group: this.group,
      },
    );
    try {
      await userGroupInvitation.save();

      this.notification.success(
        this.intl.t("service-permissions.invitation-save-success"),
      );

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute(
          "service-permissions",
          "invitations",
        ),
      );
    } catch (error) {
      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("service-permissions.invitation-save-error"),
      );

      userGroupInvitation.rollbackAttributes();
    }
  }

  save = task({ drop: true }, async (event) => {
    event.preventDefault();

    const userGroup = this.store.createRecord("user-group", {
      email: this.email,
      group: this.group,
    });

    try {
      await userGroup.save();

      this.notification.success(
        this.intl.t("service-permissions.permissions-save-success"),
      );

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute(
          "service-permissions",
          "permissions.index",
        ),
      );

      if (
        this.session.user.email === this.email &&
        this.session.groups?.retry
      ) {
        await this.session.groups.retry();
      }
    } catch (error) {
      if (
        error.errors.length === 1 &&
        error.errors[0].code === "not_found" &&
        error.errors[0].source?.pointer === "/data/attributes/email"
      ) {
        await this.invite();
      } else {
        this.notification.danger(
          parseError(error, false) ??
            this.intl.t("service-permissions.permissions-save-error"),
        );
      }

      userGroup.rollbackAttributes();
    }
  });
}
