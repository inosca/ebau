import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class LegalAppealAbility extends Ability {
  @service ebauModules;
  @service permissions;

  async canView() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "legal-appeals-read",
      );
    }

    return (
      !this.ebauModules.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }

  async canEdit() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "legal-appeals-write",
      );
    }

    return (
      !this.ebauModules.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }
}
