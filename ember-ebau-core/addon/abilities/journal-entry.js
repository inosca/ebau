import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class JournalEntryAbility extends Ability {
  @service ebauModules;
  @service permissions;

  async canAdd() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "journal-write",
      );
    }

    return !this.ebauModules.isReadOnlyRole;
  }

  async canEdit() {
    return (
      (await this.canAdd()) &&
      parseInt(this.ebauModules.userId) ===
        parseInt(this.model?.belongsTo("user").id()) &&
      parseInt(this.ebauModules.serviceId) ===
        parseInt(this.model?.belongsTo("service").id())
    );
  }
}
