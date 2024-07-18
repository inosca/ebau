import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionStepAbility extends Ability {
  @service ebauModules;
  @service permissions;

  async canEditWorkItem() {
    const isReady = this.model?.status === "READY";
    const isAddressed = this.model?.addressedGroups
      .map((id) => parseInt(id))
      .includes(parseInt(this.ebauModules.serviceId));

    if (this.permissions.fullyEnabled) {
      return (
        (await this.permissions.hasAll(
          this.ebauModules.instanceId,
          "construction-monitoring-write",
        )) &&
        isReady &&
        isAddressed
      );
    }

    return !this.ebauModules.isReadOnlyRole && isReady && isAddressed;
  }
}
