import { service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

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
    instance &&
    parseInt(instance.belongsTo("activeService").id()) === parseInt(serviceId)
  );
}

export function isInstanceService(instance, serviceId) {
  return (
    instance &&
    instance
      .hasMany("services")
      .ids()
      .map((id) => parseInt(id))
      .includes(serviceId)
  );
}

export default class InstanceAbility extends Ability {
  @service ebauModules;
  @service permissions;

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

  // BE, GR and SO
  get canCreatePaper() {
    return ["municipality-lead", "municipality-clerk"].includes(
      this.ebauModules.role,
    );
  }

  // GR and UR
  get canLinkDossiers() {
    return ["municipality", "coordination"].includes(this.ebauModules.baseRole);
  }

  async canWriteForm() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.model?.id, "form-write");
    }

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
      hasFeature("rejection.revert") &&
      isAuthority(this.model, this.ebauModules.serviceId) &&
      hasInstanceState(this.model, mainConfig.rejection?.instanceState)
    );
  }

  // instance acls
  // TODO: if complexity increases or more use cases arise, please move to instance-acl ability.
  get canEditAcl() {
    if (macroCondition(getOwnConfig().application === "be")) {
      return (
        isInstanceService(this.model, this.ebauModules.serviceId) &&
        ["municipality-lead", "municipality-clerk"].includes(
          this.ebauModules.role,
        )
      );
    }
    return isAuthority(this.model, this.ebauModules.serviceId);
  }

  async canWithdraw() {
    return await this.permissions.hasAll(this.model?.id, "instance-withdraw");
  }
}
