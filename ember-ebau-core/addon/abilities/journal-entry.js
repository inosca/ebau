import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class JournalEntryAbility extends Ability {
  @service ebauModules;

  get canAdd() {
    return !this.ebauModules.isReadOnlyRole;
  }

  get canEdit() {
    return (
      this.canAdd &&
      parseInt(this.ebauModules.userId) ===
        parseInt(this.model?.belongsTo("user").id()) &&
      parseInt(this.ebauModules.serviceId) ===
        parseInt(this.model?.belongsTo("service").id())
    );
  }
}
