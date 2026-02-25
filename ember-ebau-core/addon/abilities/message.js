import { service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
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

    const readOnlyCanSend = getOwnConfig().application === "sz";
    if (
      !this.topic ||
      (this.ebauModules.isReadOnlyRole && !readOnlyCanSend) ||
      this.ebauModules.isSupportRole
    ) {
      return false;
    }

    return this.topic.allowReplies || this.isActiveInstanceService;
  }

  async canMarkAsReadOrUnread() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        (await this.model?.topic)?.belongsTo("instance").id(),
        "communications-write",
      );
    }
    if (this.ebauModules.isSupportRole) {
      return false;
    }

    return true;
  }

  async canLinkAttachments() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        (await this.model?.topic)?.belongsTo("instance").id(),
        "communications-convert-to-document",
      );
    }

    return (
      !this.ebauModules.isReadOnlyRole &&
      !this.ebauModules.isApplicant &&
      !this.ebauModules.isSupportRole
    );
  }

  async canDeleteAttachments() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        (await this.model?.topic)?.belongsTo("instance").id(),
        "communications-delete-attachment",
      );
    }

    if (macroCondition(getOwnConfig().application === "be")) {
      return this.ebauModules.isSupportRole;
    }
    return false;
  }
}
