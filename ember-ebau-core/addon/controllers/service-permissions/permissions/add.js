import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { query } from "ember-data-resources";

import parseError from "ember-ebau-core/utils/parse-error";

export default class ServicePermissionsPermissionsAddController extends Controller {
  @service store;
  @service intl;
  @service router;
  @service ebauModules;
  @service notification;

  @tracked email;
  @tracked group;

  groups = query(this, "group", () => ({
    service_or_subservice: this.ebauModules.serviceId,
  }));

  save = dropTask(async (event) => {
    event.preventDefault();

    const userGroup = this.store.createRecord("user-group", {
      email: this.email,
      group: this.group,
    });

    try {
      await userGroup.save();

      this.notification.success(
        this.intl.t("service-permissions.permissions-save-success")
      );

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute(
          "service-permissions",
          "permissions.index"
        )
      );
    } catch (error) {
      userGroup.rollbackAttributes();

      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("service-permissions.permissions-save-error")
      );
    }
  });
}
