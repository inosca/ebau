import { service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";

export default class extends Ability {
  @service ebauModules;
  @service permissions;

  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.model?.get("instance.activeService.id"))
    );
  }

  get isActiveOrInvolvedLeadAuthority() {
    if (macroCondition(getOwnConfig().useInstanceService)) {
      let instanceServices = this.model?.get("instance.services") ?? [];
      instanceServices = instanceServices.map((service) =>
        parseInt(service.id),
      );
      return instanceServices.includes(parseInt(this.ebauModules.serviceId));
    }
    return this.isActiveInstanceService;
  }

  async canCreate() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.instanceId,
        "communications-write",
      );
    }

    return !this.ebauModules.isReadOnlyRole;
  }

  get canInvolveEntities() {
    return !this.ebauModules.isReadOnlyRole && !this.ebauModules.isApplicant;
  }

  get canDisallowReplies() {
    return !this.ebauModules.isReadOnlyRole && this.isActiveInstanceService;
  }

  get canInvolveApplicant() {
    if (this.ebauModules.isReadOnlyRole) {
      return false;
    }

    if (!this.model?.get("instance.involvedApplicants.length")) {
      return false;
    }

    const rolesWithApplicantContact =
      mainConfig.communication.rolesWithApplicantContact;

    if (
      rolesWithApplicantContact.includes("service") &&
      this.ebauModules.baseRole === "service"
    ) {
      return true;
    }

    if (
      rolesWithApplicantContact.includes("activeOrInolvedLeadAuthority") &&
      this.isActiveOrInvolvedLeadAuthority
    ) {
      return true;
    }

    return false;
  }
}
