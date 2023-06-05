import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service session;
  @service router;

  // This is set set by the case detail route
  @tracked instanceId = null;

  get serviceId() {
    return this.session.service?.id;
  }

  get isReadOnlyRole() {
    return this.session.isReadOnlyRole;
  }

  get isLeadRole() {
    return this.session.isLeadRole;
  }

  get baseRole() {
    return this.session.rolePermission;
  }

  redirectToWorkItems() {
    this.router.transitionTo("cases.detail.work-items", this.instanceId);
  }
}
