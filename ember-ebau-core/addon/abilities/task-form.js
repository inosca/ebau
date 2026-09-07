import { service } from "@ember/service";
import { Ability } from "ember-can";

import { isApplication } from "ember-ebau-core/helpers/is-application";

export default class extends Ability {
  @service ebauModules;
  @service permissions;

  async canEdit() {
    if (this.permissions.fullyEnabled) {
      const permission =
        this.writePermissionKey ??
        `form-${this.model.document.form.slug}-write`;

      const hasNewPermission = await this.permissions.hasAll(
        this.ebauModules.instanceId,
        permission,
      );

      if (hasNewPermission) {
        return true;
      }
    }

    const basePermission =
      this.model.status === "READY" &&
      !this.ebauModules.isReadOnlyRole &&
      this.model.addressedGroups.find(
        (groupId) => parseInt(groupId) === parseInt(this.ebauModules.serviceId),
      );

    if (this.task === "decision") {
      // TODO: remove with the refactoring of task form permission handling
      if (isApplication("be")) {
        return await this.permissions.hasAll(
          this.ebauModules.instanceId,
          "decision-write",
        );
      }
      return basePermission && this.ebauModules.isLeadRole;
    }

    return basePermission;
  }
}
