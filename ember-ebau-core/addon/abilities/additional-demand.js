import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class AdditionalDemandAbility extends Ability {
  @service ebauModules;
  @service session;
  @service permissions;

  get canCreate() {
    return this.session.isInternal && !this.session.isReadOnlyRole;
  }

  get canDisplay() {
    if (
      this.model.task.slug !== "fill-additional-demand" ||
      this.ebauModules.isApplicant
    ) {
      return true;
    }

    return !this.model.isReady;
  }

  async canFill() {
    if (!this.model.isReady) {
      return false;
    }

    if (this.model.task.slug === "fill-additional-demand") {
      if (this.permissions.fullyEnabled) {
        return (
          this.ebauModules.isApplicant &&
          (await this.permissions.hasAll(
            this.instanceId,
            "additional-demands-write",
          ))
        );
      }

      return this.ebauModules.isApplicant;
    }

    return (
      !this.session.isReadOnlyRole && this.model.isAddressedToCurrentService
    );
  }

  get canCancel() {
    const checkWorkItem = this.model.childCase.workItems.find(
      (workItem) =>
        workItem.task.slug === "check-additional-demand" && workItem.isReady,
    );

    return (
      this.session.isInternal &&
      !this.session.isReadOnlyRole &&
      this.model.isReady &&
      this.model.isAddressedToCurrentService &&
      !checkWorkItem
    );
  }
}
