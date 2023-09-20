import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service ebauModules;

  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.topic?.get("instance.activeService.id"))
    );
  }

  get canSend() {
    if (!this.topic || this.ebauModules.isReadOnlyRole) {
      return false;
    }

    return this.topic.allowReplies || this.isActiveInstanceService;
  }

  get canLinkAttachments() {
    return !this.ebauModules.isReadOnlyRole && !this.ebauModules.isApplicant;
  }
}
