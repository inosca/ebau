import { inject as service } from "@ember/service";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";

export default class CustomEbauModulesService extends EbauModulesService {
  @service shoebox;

  get serviceId() {
    return this.shoebox.content.serviceId;
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

  get baseRole() {
    return this.shoebox.baseRole;
  }

  get isApplicant() {
    // Since in ember-camac-ng the user is never applicant
    return false;
  }

  redirectToWorkItems() {
    window.location.replace(
      `/index/redirect-to-instance-resource/instance-id/${this.instanceId}`
    );
  }
}
