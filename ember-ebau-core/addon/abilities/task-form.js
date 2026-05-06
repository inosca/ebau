import { service } from "@ember/service";
import { Ability } from "ember-can";

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
      return basePermission && this.ebauModules.isLeadRole;
    }

    return basePermission;
  }
}
