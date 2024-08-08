import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionMonitoringAbility extends Ability {
  @service ebauModules;
  @service constructionMonitoring;
  @service permissions;

  async canInitialize() {
    const workItem = this.constructionMonitoring.controls.init;
    const isReady = workItem?.status === "READY";
    const isAddressed = workItem?.addressedGroups
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

  async canComplete() {
    const workItem = this.constructionMonitoring.controls.complete;
    const isReady = workItem?.status === "READY";
    const isAddressed = workItem?.addressedGroups
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
