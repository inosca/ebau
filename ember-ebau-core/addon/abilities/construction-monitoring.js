import { service } from "@ember/service";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";

export default class ConstructionMonitoringAbility extends Ability {
  @service store;
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

  async grAllowedToSkip() {
    const instance = this.store.peekRecord(
      "instance",
      this.ebauModules.instanceId,
    );
    const instanceState = await instance.instanceState;

    if (
      [
        mainConfig.instanceStates.subm,
        mainConfig.instanceStates["init-distribution"],
        mainConfig.instanceStates.circulation,
        mainConfig.instanceStates.decision,
      ].includes(parseInt(instanceState.id))
    ) {
      return false;
    }
  }

  async canSkip() {
    if (macroCondition(getOwnConfig().application === "gr")) {
      if (!(await this.grAllowedToSkip())) {
        return false;
      }
    }

    return this.canInitialize();
  }

  async canComplete() {
    if (macroCondition(getOwnConfig().application === "gr")) {
      if (!(await this.grAllowedToSkip())) {
        return false;
      }
    }

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
