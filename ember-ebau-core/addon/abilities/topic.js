import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";

export default class extends Ability {
  @service ebauModules;

  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.model?.get("instance.activeService.id"))
    );
  }

  get isActiveOrInvolvedLeadAuthority() {
    let instanceServices = this.model?.get("instance.services") ?? [];
    instanceServices = instanceServices.map((service) => parseInt(service.id));
    return instanceServices.includes(parseInt(this.ebauModules.serviceId));
  }

  get canCreate() {
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
