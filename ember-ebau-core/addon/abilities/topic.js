import { service } from "@ember/service";
import { getOwnConfig } from "@embroider/macros";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class extends Ability {
  @service ebauModules;
  @service permissions;
  @service session;

  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.model?.get("instance.activeService.id"))
    );
  }

  get isActiveOrInvolvedLeadAuthority() {
    if (hasFeature("noInstanceService")) {
      let instanceServices = this.model?.get("instance.services") ?? [];
      instanceServices = instanceServices.map((service) =>
        parseInt(service.id),
      );
      return instanceServices.includes(parseInt(this.ebauModules.serviceId));
    }

    return this.isActiveInstanceService;
  }

  async canCreate() {
    if (this.ebauModules.isPortal && this.session.isInternal) {
      return false;
    }

    if (
      this.session.service?.usesEchApi &&
      !hasFeature("communications.creationActivatedForEchApiUsers")
    ) {
      return false;
    }

    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.instanceId,
        "communications-write",
      );
    }

    const readOnlyCanCreate = getOwnConfig().application === "sz";
    return (
      (!this.ebauModules.isReadOnlyRole || readOnlyCanCreate) &&
      !this.ebauModules.isSupportRole
    );
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
