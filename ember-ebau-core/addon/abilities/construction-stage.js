import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionStageAbility extends Ability {
  @service ebauModules;
  @service constructionMonitoring;
  @service permissions;

  async canCreate() {
    // Check if at least one construction stage work-item (multiple-instance) is ready
    const constructionStages = this.constructionMonitoring.constructionStages;
    const hasReady = constructionStages.some(
      (stage) => stage.status === "READY",
    );
    const allAddressed = constructionStages.every((stage) =>
      stage.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId)),
    );

    if (this.permissions.fullyEnabled) {
      return (
        (await this.permissions.hasAll(
          this.ebauModules.instanceId,
          "construction-monitoring-write",
        )) &&
        hasReady &&
        allAddressed
      );
    }

    return !this.ebauModules.isReadOnlyRole && hasReady && allAddressed;
  }

  async canCancel() {
    const isRunning = this.model?.childCase.status === "RUNNING";
    const isAddressed = this.model?.addressedGroups
      .map((id) => parseInt(id))
      .includes(parseInt(this.ebauModules.serviceId));

    if (this.permissions.fullyEnabled) {
      return (
        (await this.permissions.hasAll(
          this.ebauModules.instanceId,
          "construction-monitoring-write",
        )) &&
        isRunning &&
        isAddressed
      );
    }

    return !this.ebauModules.isReadOnlyRole && isRunning && isAddressed;
  }
}
