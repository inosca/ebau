import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";

export function hasInstanceState(instance, instanceState) {
  const instanceStates = Array.isArray(instanceState)
    ? instanceState
    : [instanceState];

  const ids = instanceStates
    .map((slug) => parseInt(mainConfig.instanceStates[slug]))
    .filter(Boolean);

  return ids.includes(parseInt(instance.belongsTo("instanceState").id()));
}

export function isAuthority(instance, serviceId) {
  return (
    parseInt(instance.belongsTo("activeService").id()) === parseInt(serviceId)
  );
}

export default class InstanceAbility extends Ability {
  @service ebauModules;

  // BE
  get canSetEbauNumber() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      this.model.ebauNumber
    );
  }

  get canArchive() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      !hasInstanceState(this.model, "archived")
    );
  }

  get canChangeForm() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      mainConfig.interchangeableForms.flat().includes(this.model.calumaForm)
    );
  }

  // BE and GR
  get canCreatePaper() {
    return ["municipality-lead", "municipality-clerk"].includes(
      this.ebauModules.role,
    );
  }

  // UR
  get canLinkDossiers() {
    return (
      this.ebauModules.baseRole === "municipality" ||
      this.ebauModules.baseRole === "coordination"
    );
  }

  get canWriteForm() {
    if (macroCondition(getOwnConfig().application === "sz")) {
      return (this.model.meta?.editable || []).includes("form");
    }
    return (this.model.meta?.permissions?.main || []).includes("write");
  }

  // GR & SO
  get canCorrect() {
    return (
      // disabled until isMunicipalityLeadRole works in ember-ebau
      // (this.ebauModules.isSupportRole ||
      //   this.ebauModules.isMunicipalityLeadRole) &&
      hasInstanceState(this.model, mainConfig.correction?.allowedInstanceStates)
    );
  }

  get canFinishCorrect() {
    return (
      // disabled until isMunicipalityLeadRole works in ember-ebau
      // (this.ebauModules.isSupportRole ||
      //   this.ebauModules.isMunicipalityLeadRole) &&
      hasInstanceState(this.model, mainConfig.correction?.instanceState)
    );
  }

  // rejection
  get canReject() {
    return (
      !this.hasOpenClaims &&
      !this.hasActiveDistribution &&
      isAuthority(this.model, this.ebauModules.serviceId) &&
      hasInstanceState(this.model, mainConfig.rejection?.allowedInstanceStates)
    );
  }

  get canRevertRejection() {
    return (
      isAuthority(this.model, this.ebauModules.serviceId) &&
      hasInstanceState(this.model, mainConfig.rejection?.instanceState)
    );
  }
}
