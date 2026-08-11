import { service } from "@ember/service";
import { Ability } from "ember-can";

import { isApplication } from "ember-ebau-core/helpers/is-application";

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

    const readOnlyCanSend = isApplication("sz");
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

    if (isApplication("be")) {
      return this.ebauModules.isSupportRole;
    }
    return false;
  }
}
