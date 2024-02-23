import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionMonitoringAbility extends Ability {
  @service ebauModules;
  @service constructionMonitoring;

  get canInitialize() {
    const workItem = this.constructionMonitoring.controls.init;
    return (
      !this.ebauModules.isReadOnlyRole &&
      workItem?.status === "READY" &&
      workItem?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }

  get canComplete() {
    const workItem = this.constructionMonitoring.controls.complete;
    return (
      !this.ebauModules.isReadOnlyRole &&
      workItem?.status === "READY" &&
      workItem?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }
}
