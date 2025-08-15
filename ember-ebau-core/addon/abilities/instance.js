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

  return ids.includes(parseInt(instance?.belongsTo("instanceState").id()));
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
  @service store;

  // BE
  get canSetEbauNumber() {
    return (
      (this.ebauModules.isMunicipalityLeadRole && this.model.ebauNumber) ||
      this.ebauModules.isSupportRole
    );
  }

  get canArchive() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      !hasInstanceState(this.model, "archived")
    );
  }

  async canChangeForm() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "instance-change-form",
      );
    }

    return (
      this.ebauModules.isSupportRole || this.ebauModules.isMunicipalityLeadRole
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

  // GR & SO & BE
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
      hasInstanceState(this.model, mainConfig.correction?.instanceState) ||
      hasInstanceState(this.model, "new")
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
    if (macroCondition(getOwnConfig().application === "ur")) {
      return (
        this.ebauModules.isTrustedServiceRole ||
        this.ebauModules.isCoordinationRole ||
        isAuthority(this.model, this.ebauModules.serviceId)
      );
    }
    return isAuthority(this.model, this.ebauModules.serviceId);
  }

  async canWithdraw() {
    return await this.permissions.hasAll(this.model?.id, "instance-withdraw");
  }

  async canChangeResponsibleService() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "instance-change-responsible-service",
      );
    }

    return (
      this.ebauModules.isSupportRole ||
      (!this.ebauModules.isReadOnlyRole &&
        !hasInstanceState(
          this.model,
          mainConfig.changeResponsibleService.forbiddenInstanceStates[
            this.type
          ],
        ) &&
        // Active service is passed into the permission check
        parseInt(this.activeService?.id) === this.ebauModules.serviceId)
    );
  }

  async canAccessInstanceOnLevelRead() {
    // CAVEAT: Do NOT confuse this with a proper permission check. This ability
    // is only meant to check whether or not the "read" access level is currently
    // granted. No specific permissions can be inferred.
    if (this.permissions.fullyEnabled) {
      const instancePermission = await this.store.findRecord(
        "instance-permission",
        this.ebauModules.instanceId,
      );
      return instancePermission.currentAccessLevels.some((p) => p === "read");
    }
  }

  async canUnsubscribeResponsibleService() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "instance-unsubscribe-responsible-service",
      );
    }

    return (
      !this.ebauModules.isReadOnlyRole &&
      // Involved services are passed into the permission check
      (this.involvedServices ?? [])
        .map((service) => parseInt(service.id))
        .includes(this.ebauModules.serviceId)
    );
  }
}
