import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class JournalEntryAbility extends Ability {
  @service shoebox;

  get canEdit() {
    return !this.shoebox.isReadOnlyRole;
  }
}
