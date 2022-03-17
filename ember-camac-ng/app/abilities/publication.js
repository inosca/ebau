import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class PublicationAbility extends Ability {
  @service shoebox;

  get hasBasePermission() {
    return (
      this.shoebox.role?.startsWith("municipality") &&
      (this.model?.addressedGroups ?? []).includes(
        String(this.shoebox.content?.serviceId)
      ) &&
      !this.shoebox.isReadOnlyRole
    );
  }

  get canShowInfo() {
    return this.hasBasePermission;
  }

  get canEdit() {
    return this.hasBasePermission && this.model?.status === "READY";
  }

  get canCreate() {
    return this.hasBasePermission && this.model?.status !== "READY";
  }

  get canCancel() {
    return (
      this.hasBasePermission &&
      this.model?.status === "COMPLETED" &&
      this.model?.meta["is-published"]
    );
  }
}
