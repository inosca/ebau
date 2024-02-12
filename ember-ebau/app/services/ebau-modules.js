import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service session;
  @service router;

  // This is set set by the case detail route
  @tracked instanceId = null;

  get userId() {
    return this.session.user?.id;
  }

  get userName() {
    return this.session.user?.username;
  }

  get groupId() {
    return parseInt(this.session.group);
  }

  get serviceId() {
    return parseInt(this.session.service?.id);
  }

  get serviceModel() {
    return "service";
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
    return this.session.role?.slug;
  }

  get isApplicant() {
    return !this.session.isInternal;
  }

  get language() {
    return this.session.language;
  }

  redirectToWorkItems() {
    this.router.transitionTo("cases.detail.index", this.instanceId);
    this.router.refresh();
  }

  redirectToInstance(instanceId) {
    this.router.transitionTo("cases.detail.index", instanceId);
    this.router.refresh();
  }
}
