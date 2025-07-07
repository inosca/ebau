import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service ebauModules;
  @service permissions;

  async hasSuspensionPermission(permission) {
    if (this.ebauModules.isPortal) {
      return false;
    }

    return await this.permissions.hasAll(
      this.ebauModules.instanceId,
      `deadlines-suspensions-${permission}`,
    );
  }

  async canRead() {
    return await this.hasSuspensionPermission("read");
  }

  async canCreate() {
    return await this.hasSuspensionPermission("write");
  }

  async canEdit() {
    return await this.hasSuspensionPermission("write");
  }
}
