import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service ebauModules;
  @service permissions;

  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.topic?.get("instance.activeService.id"))
    );
  }

  async canSend() {
    if (this.permissions.fullyEnabled) {
      return (
        (this.topic.allowReplies || this.isActiveInstanceService) &&
        (await this.permissions.hasAll(
          this.topic?.get("instance.id"),
          "communications-write",
        ))
      );
    }

    if (!this.topic || this.ebauModules.isReadOnlyRole) {
      return false;
    }

    return this.topic.allowReplies || this.isActiveInstanceService;
  }

  async canMarkAsReadOrUnread() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model.belongsTo("instance").id(),
        "communications-write",
      );
    }

    return true;
  }

  get canLinkAttachments() {
    return !this.ebauModules.isReadOnlyRole && !this.ebauModules.isApplicant;
  }
}
