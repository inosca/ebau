import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionMonitoringAbility extends Ability {
  @service store;
  @service ebauModules;
  @service constructionMonitoring;
  @service permissions;

  #hasBasePermission(key) {
    const workItem = this.constructionMonitoring.controls[key];

    return (
      workItem?.status === "READY" &&
      workItem?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }

  async canInit() {
    if (!this.#hasBasePermission("init")) {
      return false;
    }

    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "construction-monitoring-init",
      );
    }

    return !this.ebauModules.isReadOnlyRole;
  }

  async canSkip() {
    if (!this.#hasBasePermission("init")) {
      return false;
    }

    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "construction-monitoring-skip",
      );
    }

    return !this.ebauModules.isReadOnlyRole;
  }

  async canComplete() {
    if (!this.#hasBasePermission("complete")) {
      return false;
    }

    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "construction-monitoring-complete",
      );
    }

    return !this.ebauModules.isReadOnlyRole;
  }
}
