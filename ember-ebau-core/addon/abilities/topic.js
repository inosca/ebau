import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service ebauModules;

  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.model?.get("instance.activeService.id"))
    );
  }

  get isInstanceService() {
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
    return !this.ebauModules.isReadOnlyRole && this.isInstanceService;
  }
}
