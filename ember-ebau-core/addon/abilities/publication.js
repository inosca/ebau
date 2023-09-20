import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class PublicationAbility extends Ability {
  @service ebauModules;

  get hasBasePermission() {
    return (
      this.ebauModules.baseRole === "municipality" &&
      !this.ebauModules.isReadOnlyRole
    );
  }

  get isAddressed() {
    return (this.model?.addressedGroups ?? []).includes(
      String(this.ebauModules.serviceId),
    );
  }

  get canShowInfo() {
    return this.hasBasePermission && this.isAddressed;
  }

  get canEdit() {
    return (
      this.hasBasePermission &&
      this.isAddressed &&
      this.model?.status === "READY"
    );
  }

  get canCreate() {
    return this.hasBasePermission && this.model?.status !== "READY";
  }

  get canCancel() {
    return (
      this.hasBasePermission &&
      this.isAddressed &&
      this.model?.status === "COMPLETED" &&
      this.model?.meta["is-published"]
    );
  }
}
