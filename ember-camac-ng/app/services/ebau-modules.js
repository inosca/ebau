import { service } from "@ember/service";
import EbauModulesService from "ember-ebau-core/services/ebau-modules";
import { trackedFunction } from "reactiveweb/function";

export default class CustomEbauModulesService extends EbauModulesService {
  @service shoebox;
  @service fetch;
  @service store;

  #additionalData = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      "/api/v1/me?include=groups,groups.role,groups.service,groups.service.service_group",
    );
    const result = await response.json();

    this.store.pushPayload(result);

    return {
      service: this.store.peekRecord("service", this.serviceId),
      serviceGroup: this.store.peekRecord(
        "public-service-group",
        this.shoebox.content.serviceGroupId,
      ),
    };
  });

  get serviceSlug() {
    return this.#additionalData.value?.service?.slug;
  }

  get serviceGroupSlug() {
    return this.#additionalData.value?.serviceGroup?.slug;
  }

  get serviceGroupName() {
    return this.#additionalData.value?.serviceGroup?.name;
  }

  get userId() {
    return this.shoebox.content.userId;
  }

  get userName() {
    return this.shoebox.content.username;
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

  get isTrustedServiceRole() {
    return this.shoebox.isTrustedServiceRole;
  }

  get isCoordinationRole() {
    return this.shoebox.isCoordinationRole;
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

  redirectToCaseWorkItems = () => {
    window.location.replace(
      `/index/redirect-to-instance-resource/instance-id/${this.instanceId}`,
    );
  };

  redirectToInstance = (instanceId) => {
    window.location.replace(
      `/index/redirect-to-instance-resource/instance-id/${instanceId}`,
    );
  };

  redirectToInstanceForm = (instanceId) => {
    window.location.replace(
      `/index/redirect-to-instance-resource/instance-id/${instanceId}/form`,
    );
  };

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
