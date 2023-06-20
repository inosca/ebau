import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service session;
  @service router;

  // This is set set by the case detail route
  @tracked instanceId = null;

  get groupId() {
    console.log("TODO works?", this.session.group);
    return this.session.group?.id;
  }

  get serviceId() {
    return this.session.service?.id;
  }

  get isReadOnlyRole() {
    return this.session.isReadOnlyRole;
  }

  get isLeadRole() {
    return this.session.isLeadRole;
  }

  get isSupportRole() {
    return this.session.isSupport;
  }

  get isMunicipalityLeadRole() {
    return this.session.isMunicipalityLeadRole;
  }

  get baseRole() {
    return this.session.rolePermission;
  }

  get role() {
    return this.session.role;
  }

  get portalURL() {
    // TODO how to do ENV-specific config?
    return "";
  }

  get isApplicant() {
    return !this.session.isInternal;
  }

  get language() {
    return this.session.language;
  }

  redirectToWorkItems() {
    this.router.transitionTo("cases.detail.work-items", this.instanceId);
  }
}
