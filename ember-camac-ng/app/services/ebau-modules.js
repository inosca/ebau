import { inject as service } from "@ember/service";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service shoebox;

  get userId() {
    return this.shoebox.content.userId;
  }

  get groupId() {
    return this.shoebox.content.groupId;
  }

  get serviceId() {
    return this.shoebox.content.serviceId;
  }

  get role() {
    return this.shoebox.role;
  }

  get instanceId() {
    return this.shoebox.content.instanceId;
  }

  get isReadOnlyRole() {
    return this.shoebox.isReadOnlyRole;
  }

  get isLeadRole() {
    return this.shoebox.isLeadRole;
  }

  get isSupportRole() {
    return this.shoebox.isSupportRole;
  }

  get isMunicipalityLeadRole() {
    return this.shoebox.isMunicipalityLeadRole;
  }

  get baseRole() {
    return this.shoebox.baseRole;
  }

  get isApplicant() {
    // Since in ember-camac-ng the user is never applicant
    return false;
  }

  get language() {
    return this.shoebox.content.language;
  }

  redirectToWorkItems() {
    window.location.replace(
      `/index/redirect-to-instance-resource/instance-id/${this.instanceId}`,
    );
  }

  // careful: only works in ember-camac-ng!
  // for modern apps use task.meta.directLink instead
  get directLinkConfig() {
    return this.shoebox.content.config.directLink;
  }

  // careful: only works in ember-camac-ng!
  get resourceId() {
    return this.shoebox.content.resourceId;
  }
}
