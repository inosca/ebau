import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service ebauModules;

  get canEdit() {
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
