import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service shoebox;

  get canEdit() {
    const basePermission =
      this.model.status === "READY" &&
      !this.shoebox.isReadOnlyRole &&
      this.model.addressedGroups.find(
        (groupId) =>
          parseInt(groupId) === parseInt(this.shoebox.content.serviceId)
      );

    if (this.task === "decision") {
      return basePermission && this.shoebox.isLeadRole;
    }

    return basePermission;
  }
}
