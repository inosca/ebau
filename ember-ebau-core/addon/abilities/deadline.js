import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service ebauModules;
  @service permissions;

  async hasDeadlinePermission(permission) {
    if (this.ebauModules.isPortal) {
      return false;
    }

    return await this.permissions.hasAll(
      this.ebauModules.instanceId,
      `deadlines-deadlines-${permission}`,
    );
  }

  async canRead() {
    return await this.hasDeadlinePermission("read");
  }

  async canEdit() {
    return await this.hasDeadlinePermission("write");
  }
}
