import { service } from "@ember/service";
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

  /** can create new drafts */
  get canCreate() {
    return this.hasBasePermission && this.model?.status !== "READY";
  }

  /** can submit a draft */
  get canSubmit() {
    return this.hasBasePermission && this.model?.status === "READY";
  }

  /** can cancel/unpublish already completed workitems */
  get canCancel() {
    return (
      this.hasBasePermission &&
      this.isAddressed &&
      this.model?.status === "COMPLETED" &&
      this.model?.meta["is-published"]
    );
  }

  /** can delete drafts */
  get canDelete() {
    return this.hasBasePermission && this.model?.status === "READY";
  }
}
