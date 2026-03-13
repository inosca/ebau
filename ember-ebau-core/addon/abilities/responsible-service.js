import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ResponsibleServiceAbility extends Ability {
  @service ebauModules;
  @service permissions;

  async canEdit() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "responsible-write",
      );
    }

    return !this.ebauModules.isReadOnlyRole;
  }
}
